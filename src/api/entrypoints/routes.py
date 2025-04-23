import asyncio
from fastapi import APIRouter, Request
from src.addons.integrations.plugins.capsule import *
from src.core.dependencies import AnnotatedPm, AnnotatedClientId,AnnotatedSettings
from src.modules.handlers import save_token_data, get_access_token_from_header,save_contacts
from src.config.settings import AppSettings
from src.modules.queries import read_json, write_json
from src.core.exceptions import *

router = APIRouter(prefix="/intergrations", tags=["Integrations"])


@router.get("/")
async def get_authorization_url(
    request: Request, pm: AnnotatedPm,settings: AnnotatedSettings, name: str | None = None
):

    tasks = pm.hook.get_crm_authorization_url(
        name=name,
        settings=settings
    )
    
    url = await asyncio.gather(*tasks)
    return {"authorization_url": url}


@router.get("/token/")
async def get_users_token(
    request: Request,
    sub_domain: str,
):
    print("token endpoint")
    json_data = read_json("tokens.json")
    data = json_data.get(sub_domain, None)
    if not data:
        raise InvalidUserException("Invalid User")

    return {"access_token": data.get("access_token")}


@router.get("/contacts/")
async def get_contact_resource(
    request: Request,
    pm: AnnotatedPm,
    settings: AnnotatedSettings,
    name: str,
    page: int,
    perPage: int
):
    access_token = get_access_token_from_header(request)
    tasks = pm.hook.get_contacts(
        name=name,
        settings=settings,
        access_token=access_token,
        page=page,
        perPage=perPage
    )
    contacts=await asyncio.gather(*tasks)

    save_contacts("contacts.json", contacts)
    return contacts
