from fastapi import APIRouter,Request
from src.addons.implementations import *
from src.addons.hookspecs import *
from src.database.handlers import check_valid_state,save_token_date
from fastapi.responses import JSONResponse
from src.core.exceptions import *
from src.core.dependencies import AnnotatedPm





router = APIRouter(prefix="/callbacks",tags = ["Callbacks"])



@router.get("/integrations/{name}")
async def get_token_from_crm(
    request: Request,
    pm:AnnotatedPm,
    name:str,
    code: str, 
    state: str):

    print("callbacks endpoint called")
    

    if not check_valid_state(state):
        raise InvalidStateException("Invalid State")
    
    pm = request.app.state.pm

    results = pm.hook.get_access_token(
        name=name,
        client_id=request.app.state.settings.crmconfig.client_id,
        code=code)
    
    token_response = [await result for result in results]
    data = {
        token_response[0]["subdomain"]:{
            "crm":name,
            **token_response[0]
        }
    }
    if not save_token_date("tokens.json",data):
        raise UnableToSaveException("Unable to save token data")
    return token_response[0]
