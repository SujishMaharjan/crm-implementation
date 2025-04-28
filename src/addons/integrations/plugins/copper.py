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




class CapsuleCrmPlugin:

    @hookimpl
    async def get_crm_authorization_url(self, name, settings: AppSettings):
        if name == "coppercrm" or name == None:
            base_url = "https://app.copper.com/oauth/authorize"
            state = generate_store_state()
            params = {
                "response_type": "code",
                "client_id": settings.copper.client_id,
                "redirect_uri": f"http://localhost:8000/callbacks/integrations/coppercrm",
                "scope": "developer/v1/all",
                "state": state,
            }
            query_string = urlencode(params)
            full_uri = f"{base_url}?{query_string}"

            return {"coppercrm": full_uri}
        
    @hookimpl
    async def get_access_token(self, name, code, state, settings: AppSettings):
        if name == "capsulecrm":

            check_valid_state(state)

            token_url = "https://api.capsulecrm.com/oauth/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            data = {
                "code": code,
                "client_id": settings.capsule.client_id,
                "grant_type": "authorization_code",
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                response_data["created_at"] = datetime.utcnow().isoformat()
                response_data["crm_subdomain"] = response_data["subdomain"]
                response_data["crm_name"] = name
                return response_data
