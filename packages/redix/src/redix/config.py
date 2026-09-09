from functools import lru_cache

from pydantic_settings import BaseSettings

DEFAULT_REDIS_URL = "redis://localhost:6379"


class Settings(BaseSettings):
    redis_url: str = DEFAULT_REDIS_URL


@lru_cache
def get_settings() -> Settings:
    return Settings()
