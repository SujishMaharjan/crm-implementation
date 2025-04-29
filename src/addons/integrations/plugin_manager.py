import pluggy
from src.addons.integrations import hookspecs
from src.addons.integrations.plugins import capsule,pipedrive

def init_plugin_manager():
    pm = pluggy.PluginManager("CRMS")
    pm.add_hookspecs(hookspecs.CrmSpec)
    pm.register(capsule.CapsuleCrmPlugin())
    pm.register(pipedrive.PipedriveCrmPlugin())
    return pm