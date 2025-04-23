from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class CapsuleSettings(BaseModel):
    client_id: str
    client_secret: str

class AppSettings(BaseSettings):
    capsule: CapsuleSettings  

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
