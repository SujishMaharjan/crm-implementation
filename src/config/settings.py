from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class CrmSettings(BaseModel):
    client_id: str
    client_secret: str

class DatabaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: int
    name: str


class AppSettings(BaseSettings):
    crmconfig: CrmSettings# = Field(validation_alias='dabase: DatabaseSettings
    # database: DatabaseSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
        )



