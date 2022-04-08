from functools import lru_cache
from typing import Any, Dict, List

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Coding Kittens"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    # This Redis instance is tuned for durability.
    REDIS_DATA_URL: str = "redis://redis:6379"

    # This Redis instance is tuned for cache performance.
    REDIS_CACHE_URL: str = "redis://redis:6379"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
