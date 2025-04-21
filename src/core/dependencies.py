from fastapi import Depends,Request
from typing import Annotated
import pluggy
from src.core.utils import get_plugin_manager


AnnotatedPm = Annotated[pluggy.PluginManager,Depends(get_plugin_manager)]


