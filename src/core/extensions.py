from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from fastapi import Depends, Request
from src.config.settings import DatabaseSettings


Base = declarative_base()


def create_db_engine(database: DatabaseSettings):
    engine = create_engine(
        f"postgresql://{database.user}:{database.password}@{database.host}:{database.port}/{database.name}"
    )
    return engine


def init_db(engine):
    Base.metadata.create_all(bind=engine)


def get_db_session(request: Request):
    engine = request.app.state.engine
    with Session(engine) as session:
        yield session
