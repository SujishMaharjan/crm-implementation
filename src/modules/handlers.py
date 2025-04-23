import secrets
from datetime import datetime, timedelta
from src.modules.queries import write_json, read_json
from fastapi.responses import JSONResponse
from src.core.exceptions import *
from fastapi import Request
from datetime import datetime, timedelta
import random,string


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

def save_token_data(filename, datas):
    json_db_data = read_json(filename)
    for data in datas:
        json_db_data[data["subdomain"]]= data
    write_json(filename, json_db_data)
    return True

def save_contacts(filename, datas):
    json_db_data = read_json(filename)
    for data in datas:
        json_db_data.update(data)
    write_json(filename, json_db_data)
    return True



def get_refresh_token(access_token):

    json_data = read_json("tokens.json")
    token_data = next((sub_dict for sub_dict in json_data.values() if sub_dict["access_token"] == access_token), None)
    if not token_data:
        raise InvalidTokenException("Invalid Token")
    return token_data.get("refresh_token")


def check_if_access_token_expired(access_token)-> bool:
    json_data = read_json("tokens.json")
    data = next((sub_dict for sub_dict in json_data.values() if sub_dict["access_token"] == access_token), None)
    if not data:
        raise InvalidTokenException("Invalid Token")
    current_time = datetime.utcnow()
    expiry_time = datetime.fromisoformat(data["created_at"]) + timedelta(seconds=data["expires_in"])
    return current_time > expiry_time


def create_current_expiry_time_timedate_format(seconds):
    current_time = datetime.utcnow()
    expiry_time = current_time + timedelta(seconds=seconds)
    return expiry_time.isoformat()


def update_token_data(access_token_data)->bool:
    access_token_data["created_at"]=datetime.utcnow().isoformat()
    json_data = read_json("tokens.json")
    sub_domain = access_token_data.get("subdomain", None)
    json_data[sub_domain] = access_token_data
    write_json("tokens.json", json_data)
    return True


def generate_state():
    state = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    return state
