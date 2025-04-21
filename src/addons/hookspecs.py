import pluggy

hookspec = pluggy.HookspecMarker("CRMS")

class CrmSpec:

    @hookspec
    def get_crm_authorization_url(self,name,client_id,scope,state): ...
    """Returns authorization_code"""

    @hookspec
    async def get_access_token(self,name,client_id,code): ...

    @hookspec
    def get_resource(): ...