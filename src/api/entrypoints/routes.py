from fastapi import APIRouter,Request
from typing import Literal
from src.addons.implementations import *
from src.database.handlers import generate_state






router = APIRouter(
    prefix="/intergrations",
    tags = ["Integrations"]
)




@router.get("/")
async def get_authorization_url(
    request: Request,
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








