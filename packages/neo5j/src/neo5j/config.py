from functools import lru_cache

from pydantic_settings import BaseSettings

DEFAULT_DATABASE_URL = "neo4j://localhost:7687"
DEFAULT_DATABASE_USERNAME = "neo4j"
DEFAULT_DATABASE_PASSWORD = "mysecretpassword"


class Settings(BaseSettings):
    database_url: str = DEFAULT_DATABASE_URL
    db_username: str = DEFAULT_DATABASE_USERNAME
    db_password: str = DEFAULT_DATABASE_PASSWORD


@lru_cache
def get_settings() -> Settings:
    return Settings()
