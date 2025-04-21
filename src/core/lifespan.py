import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config.settings import AppSettings
from src.core.extensions import create_db_engine,init_db
from src.addons.implementations import init_plugin_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Server ....")
    
    app.state.settings = AppSettings()
    app.state.engine = await asyncio.to_thread(create_db_engine,app.state.settings.database)
    await asyncio.to_thread(init_db, app.state.engine)
    app.state.pm = init_plugin_manager()
    app.state.settings = AppSettings()
    print(app.state.settings)
    yield
    
    print("Stopping Server ....")

