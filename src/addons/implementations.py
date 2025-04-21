import pluggy,httpx
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
from fastapi import Request
from src.core.exceptions import *
from src.addons.hookspecs import CrmSpec

hookimpl = pluggy.HookimplMarker("CRMS")





class CapsuleCrmPlugin:


    @hookimpl
    def get_crm_authorization_url(self,name,client_id,scope,state):
        if name == "capsulecrm":
            base_url = "https://api.capsulecrm.com/oauth/authorise"



            redirect_base = "http://localhost:8000/callbacks/integrations"
            redirect_with_param = f"{redirect_base}?name=capsulecrm"
            
            # http://127.0.0.1:8000/intergrations?name=capsulecrm
            params = {
                "response_type":"code",
                "client_id":client_id,
                "redirect_uri":f"http://localhost:8000/callbacks/integrations/{name}",
                "scope": scope,
                "state": state
            }
            print(params["redirect_uri"])
            query_string = urlencode(params)
            
            full_uri = f"{base_url}?{query_string}"

            return full_uri


    @hookimpl
    async def get_access_token(self,name,client_id,code):
        if name == "capsulecrm":
            token_url = "https://api.capsulecrm.com/oauth/token"

            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {
                "code":code,
                "client_id" : client_id,
                "grant_type" : "authorization_code"
            }
            

            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data,headers=headers)
                response.raise_for_status()
                return response.json()
            
            




    @hookimpl
    async def get_contacts(self,name,access_token):
        if name == "capsulecrm":
            headers = {"Authorization": f"Bearer {access_token}"}

            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.capsulecrm.com/api/v2/parties", headers=headers)
            return response.json()
            



def init_plugin_manager():
    pm = pluggy.PluginManager("CRMS")
    pm.add_hookspecs(CrmSpec)
    pm.register(CapsuleCrmPlugin())
    return pm


