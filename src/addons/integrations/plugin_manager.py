import pluggy
from src.addons.integrations import hookspecs


def init_plugin_manager():
    pm = pluggy.PluginManager("CRMS")
    pm.add_hookspecs(hookspecs.CrmSpec)
    return pm