from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.addons.integrations.plugin_manager import init_plugin_manager
from src.config.settings import AppSettings
from src.api.entrypoints.routes import router
from src.api.entrypoints.callbacks import router as callback_route
from src.core.middlewares import ExceptionMiddleware,CleanUpStatesMiddleware
from src.addons.integrations.plugins import capsule,kommo,keap,pipedrive


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Server ....")

    app.state.pm = init_plugin_manager()
    #registering pluggins
    app.state.pm.register(capsule.CapsuleCrmPlugin())
    # app.state.pm.register(kommo.KommoCrmPlugin())
    # app.state.pm.register(keap.KeapCrmPlugin())
    app.state.pm.register(pipedrive.PipedriveCrmPlugin())
    
    app.state.settings = AppSettings()
    print(app.state.settings)
    yield

    print("Stopping Server ....")


def init_app():
    app = FastAPI(lifespan=lifespan)

    # add_middlewares
    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(CleanUpStatesMiddleware)
    
    # add routes
    app.include_router(router)
    app.include_router(callback_route)

    return app


app = init_app()


