import pluggy
from src.config.settings import AppSettings

hookspec = pluggy.HookspecMarker("CRMS")


class CrmSpec:

    @hookspec
    async def get_crm_authorization_url(self,settings: AppSettings): ...
    """Returns authorization_code"""

    @hookspec
    async def get_access_token(self, name,state,code,settings:AppSettings): ...

    @hookspec
    async def get_contacts(self, name, settings:AppSettings, access_token, page, perPage): ...

    @hookspec
    async def regenerate_access_token(self, name, refresh_token, settings:AppSettings): ...
