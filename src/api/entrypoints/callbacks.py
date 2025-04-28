from fastapi import APIRouter, Request
from src.addons.integrations.plugins.capsule import *
from src.addons.integrations.hookspecs import *
from src.modules.handlers import check_valid_state, save_token_data,create_current_expiry_time_timedate_format
from fastapi.responses import JSONResponse
from src.core.exceptions import *
from src.core.dependencies import AnnotatedPm, AnnotatedClientId,AnnotatedSettings
import asyncio

router = APIRouter(prefix="/callbacks", tags=["Callbacks"])


@router.get("/integrations/{name}")
async def get_token_from_crm(
    request: Request,
    pm: AnnotatedPm,
    settings: AnnotatedSettings,
    name: str,
    code: str,
    state: str,
):

    tasks = pm.hook.get_access_token(
        name=name,
        code=code,
        state=state,
        settings=settings

    ) 
    # return {"code": code}
    token_response = await asyncio.gather(*tasks)
    save_token_data("tokens.json",token_response)

    return {"message":"Crm Connected Successfully"}




    




