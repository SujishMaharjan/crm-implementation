import asyncio
from fastapi import APIRouter, Request
from src.addons.integrations.plugins.capsule import *
from src.core.dependencies import AnnotatedPm, AnnotatedClientId,AnnotatedSettings
from src.modules.handlers import (
    save_token_data,
    get_access_token_from_header,
    save_contacts,
    fetch_access_token_by_subdomain
)
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
async def get_users_token_resource(
    request: Request,
    crm_name:str,
    sub_domain: str
):
    access_token = fetch_access_token_by_subdomain(crm_name,sub_domain)
    return {"access_token": access_token}


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
