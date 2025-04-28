
import pluggy, httpx, asyncio
from datetime import datetime
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from fastapi import Request
from src.core.exceptions import *
from src.addons.integrations.hookspecs import CrmSpec
from src.modules.handlers import (
    check_if_access_token_expired,
    get_refresh_token,
    generate_store_state,
    update_token_data,
    check_valid_state,
)
from src.config.settings import AppSettings
from src.addons.integrations.plugins import hookimpl



class KeapCrmPlugin:

    @hookimpl
    async def get_crm_authorization_url(self, name, settings: AppSettings):
        if name == "keapcrm" or name == None:
            base_url = "https://accounts.infusionsoft.com/app/oauth/authorize"

            state = generate_store_state()
            params = {
                "client_id": settings.kommo.client_id,
                "redirect_uri": f"http://localhost:8000/callbacks/integrations/keapcrm",
                "response_type": "code",
                "scope":"full"
            }
            query_string = urlencode(params)
            full_uri = f"{base_url}?{query_string}"

            return {"keap crm": full_uri}

    @hookimpl
    async def get_access_token(self, name, code, state, settings: AppSettings):
        if name == "kommocrm":

            check_valid_state(state)

            token_url = "https://www.kommo.com/oauth2/access_token"
            headers = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            payload = {

                "client_id": settings.kommo.client_id,
                "client_secret": settings.kommo.client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri":f"http://localhost:8000/callbacks/integrations/kommocrm"
            }

            async with httpx.AsyncClient() as client:
                breakpoint()
                response = await client.post(token_url, json=payload, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                response_data["created_at"] = datetime.utcnow().isoformat()
                return response_data