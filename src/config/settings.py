from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class BaseIntegrationSettings(BaseModel):
    client_id: str
    client_secret: str

class CapsuleSettings(BaseIntegrationSettings):...

class KommoSettings(BaseIntegrationSettings):...

class KeapSettings(BaseIntegrationSettings): ...

class CopperSettings(BaseIntegrationSettings): ...

class PipedriveSettings(BaseIntegrationSettings): ...


class AppSettings(BaseSettings):
    capsule: CapsuleSettings  
    kommo: KommoSettings
    keap: KeapSettings
    copper: CopperSettings
    pipedrive: PipedriveSettings

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
