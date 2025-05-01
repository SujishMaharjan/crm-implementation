from fastapi import Depends, Request
from typing import Annotated
import pluggy
from src.config.settings import AppSettings


def get_client_id(request: Request):
    return request.app.state.settings.crmconfig.client_id

def get_settings(request: Request):
    return request.app.state.settings

def get_plugin_manager(request: Request):
    return request.app.state.pm


# use meaning full name
AnnotatedPlugginManager = Annotated[pluggy.PluginManager, Depends(get_plugin_manager)]
AnnotatedClientId = Annotated[str, Depends(get_client_id)]
AnnotatedSettings = Annotated[AppSettings, Depends(get_settings)]
