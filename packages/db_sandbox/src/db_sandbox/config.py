from functools import lru_cache

from pydantic_settings import BaseSettings

DEFAULT_DATABASE_URL = (
    "postgresql://postgres:mysecretpassword@localhost:5430/sandbox"
)
OLLAMA_HOST_URL = "http://localhost:11434"


class Settings(BaseSettings):
    database_url: str = DEFAULT_DATABASE_URL
    ollama_host_url: str = OLLAMA_HOST_URL


@lru_cache
def get_settings() -> Settings:
    return Settings()
