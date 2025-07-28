# app/core/settings.py

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    debug: bool = True

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    stripe_secret_key: str
    stripe_webhook_secret: str

    base_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
