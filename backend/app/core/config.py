from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "creator-os"
    app_env: str = "development"

    # Douyin official OAuth app credentials.
    douyin_client_key: str = ""
    douyin_client_secret: str = ""
    douyin_redirect_uri: str = ""

    default_provider_mode: str = "platform"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
