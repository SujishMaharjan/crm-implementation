import secrets
from datetime import datetime, timedelta
from src.modules.queries import write_json, read_json
from fastapi.responses import JSONResponse
from src.core.exceptions import *
from fastapi import Request
from datetime import datetime, timedelta
import random,string,pluggy



def generate_store_state(expiry_minutes=5):
    try:
        state = generate_state()
        # state = secrets.token_urlsafe(16)
        created_at = datetime.utcnow()
        expiry_at = created_at + timedelta(minutes=expiry_minutes)
        data = {
            state:{
            "state": state,
            "created_at": created_at.isoformat(),
            "expiry_at": expiry_at.isoformat()  
            }  
        }
        if save_state_data("states.json", data):
            return state
    except Exception as e:
        return JSONResponse(content={"detail": str(e)})


def get_access_token_from_header(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        raise InvalidTokenException("Invalid Token")
    access_token = auth_header.removeprefix("Bearer ").strip()
    return access_token


def check_valid_state(state)->bool:
    data = read_json("states.json")
    if not state in data:
        raise InvalidStateException("detail:Invalid state")
    expiry_at = datetime.fromisoformat(data[state]["expiry_at"])
    if datetime.utcnow() > expiry_at:
        raise InvalidStateException("detail:State is Expired")
    return True

def save_state_data(filename,data):
    json_db_data = read_json(filename)
    json_db_data.update(data)
    write_json(filename, json_db_data)
    return True

def save_token_data(filename,datas):
    tokens = read_json(filename)
    for data in datas:
        if data is None:
            continue
        sub_domain=data.get("crm_subdomain")
        crm_name=data.get("crm_name")
        if crm_name not in tokens:
            tokens[crm_name] = {}
        tokens[crm_name][sub_domain] = data
    write_json(filename, tokens)
    return True
# def save_token_data(filename,name,datas):
#     json_db_data = read_json(filename)
#     for data in datas:
#         json_db_data[name]=data
#     write_json(filename, json_db_data)
#     return True


def save_contacts(filename, datas):
    json_db_data = read_json(filename)
    for data in datas:
        if data is None:
            continue
        json_db_data.update(data)
    write_json(filename, json_db_data)
    return True
# def save_contacts(filename, datas):
#     json_db_data = read_json(filename)
#     for data in datas:
#         json_db_data.update(data)
#     write_json(filename, json_db_data)
#     return True



def get_refresh_token(name,access_token):

    json_data = read_json("tokens.json")
    token_data = next((sub_dict for sub_dict in json_data[name].values() if sub_dict["access_token"] == access_token), None)
    if not token_data:
        raise InvalidTokenException("Invalid Token")
    return token_data.get("refresh_token")


def check_if_access_token_expired(crm_name,access_token)-> bool:
    json_data = read_json("tokens.json")
    data = next((sub_dict for sub_dict in json_data[crm_name].values() if sub_dict["access_token"] == access_token), None)
    if not data:
        raise InvalidTokenException("Invalid Token")
    current_time = datetime.utcnow()
    expiry_time = datetime.fromisoformat(data["created_at"]) + timedelta(seconds=data["expires_in"])
    return current_time > expiry_time


def create_current_expiry_time_timedate_format(seconds):
    current_time = datetime.utcnow()
    expiry_time = current_time + timedelta(seconds=seconds)
    return expiry_time.isoformat()


def update_token_data(name,access_token_data)->bool:
    access_token_data["created_at"]=datetime.utcnow().isoformat()
    json_data = read_json("tokens.json")
    sub_domain = access_token_data.get("subdomain", None)
    json_data[name][sub_domain] = access_token_data
    write_json("tokens.json", json_data)
    return True


def generate_state():
    state = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    return state

def fetch_access_token_by_subdomain(crm_name,sub_domain):
    json_db_data = read_json("tokens.json")
    return json_db_data[crm_name][sub_domain]["access_token"]




def get_crm_names_list(pm: pluggy.PluginManager):
    crm_names = [plugin.crm_name for plugin in pm.get_plugins()]
    if not crm_names:
        raise NotFoundException("No any Registerd Plugins")
    return crm_names


def check_valid_crm_names(name:list,crm_names:list):
    invalid_names = set(name)-set(crm_names)
    if invalid_names:
        raise InvalidInputException(f"Invalid Crm names: {" ".join(invalid_names)}")
    return True

def get_remove_plugin_list(remove_list):

    return 