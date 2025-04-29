from fastapi import Depends, Request
from typing import Annotated
import pluggy
from src.core.utils import get_plugin_manager
from src.config.settings import AppSettings


def get_client_id(request: Request):
    return request.app.state.settings.crmconfig.client_id

def get_settings(request: Request):
    return request.app.state.settings

# use meaning full name
AnnotatedPm = Annotated[pluggy.PluginManager, Depends(get_plugin_manager)]
AnnotatedClientId = Annotated[str, Depends(get_client_id)]
AnnotatedSettings = Annotated[AppSettings, Depends(get_settings)]
