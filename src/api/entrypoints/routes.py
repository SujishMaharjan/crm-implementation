from fastapi import APIRouter,Request,Depends
from typing import Literal,Annotated
from src.addons.implementations import *
from src.database.handlers import generate_state
from src.core.dependencies import AnnotatedPm
from src.database.queries import read_json
from fastapi.security import OAuth2PasswordBearer
from src.core.exceptions import *

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/intergrations/token")



router = APIRouter(
    prefix="/intergrations",
    tags = ["Integrations"]
)




@router.get("/")
async def get_authorization_url(
    request: Request,
    pm: AnnotatedPm,
    name: Literal["copper", "capsulecrm"]
):

    pm = request.app.state.pm
    # breakpoint()
    url = pm.hook.get_crm_authorization_url(
        name=name,
        response_type="code",
        client_id=request.app.state.settings.crmconfig.client_id,
        scope="read write",
        state=generate_state()
        )
    return {"authorization_url":url}





@router.get("/token/")
async def get_users_token(
    request:Request,
    user_name: str,
    ):
    print("token endpoint")
    # breakpoint()
    json_data = read_json("tokens.json")
    access_token = json_data.get(user_name, None).get("access_token")
    if not access_token:
        raise InvalidUserException("Invalid User")
    
    return {"access_token": access_token.get("access_token")}



    






@router.get("/contacts/")
async def get_contact_resource(
    request:Request,
    pm:AnnotatedPm,
    name: str
):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        raise InvalidTokenException("Invalid Token")
    access_token  = auth_header.removeprefix("Bearer ").strip()

    results = pm.hook.get_contacts(
        name=name,
        access_token=access_token)
    token_response = [await result for result in results]
    return token_response[0]
    
    
    






