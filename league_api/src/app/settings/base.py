from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings
from .constants import API_KEY, SENTRY_DSN


class Settings(BaseSettings):
    API_KEY: str = API_KEY
    SENTRY_DSN: str = SENTRY_DSN
    DEBUG: bool = False

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
