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
from src.api.entrypoints.models import CrmType



class CapsuleCrmPlugin:
    crm_name = CrmType.capsule

    @hookimpl
    async def get_crm_authorization_url(self, settings: AppSettings):
        
        base_url = "https://api.capsulecrm.com/oauth/authorise"
        state = generate_store_state()
        params = {
            "response_type": "code",
            "client_id": settings.capsule.client_id,
            "redirect_uri": f"http://localhost:8000/callbacks/integrations/capsulecrm",
            "scope": "read write",
            "state": state,
        }
        query_string = urlencode(params)
        full_uri = f"{base_url}?{query_string}"

        return {"capsulecrm": full_uri}

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

    @hookimpl
    async def get_contacts(
        self, name, settings: AppSettings, access_token, page, perPage
    ):
        if name == "capsulecrm":

            if check_if_access_token_expired(crm_name=name,access_token=access_token):

                access_token_data = await asyncio.gather(
                    self.regenerate_access_token(
                        name=name,
                        refresh_token=get_refresh_token(name,access_token),
                        client_id=settings.capsule.client_id,
                    )
                )
        
                update_token_data(name,access_token_data[0])
                access_token = access_token_data[0].get("access_token")

            headers = {"Authorization": f"Bearer {access_token}"}
            base_url = "https://api.capsulecrm.com/api/v2/parties"
            params = {"page": page, "perPage": perPage}
            url = f"{base_url}?{urlencode(params)}"

            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=headers)
                return {name:response.json()}

    @hookimpl
    async def regenerate_access_token(self, name, refresh_token, settings:AppSettings):
        token_url = "https://api.capsulecrm.com/oauth/token"

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "refresh_token": refresh_token,
            "client_id": settings.capsule.client_id,
            "grant_type": "refresh_token",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
