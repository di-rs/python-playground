from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from neo4j import Driver, GraphDatabase

from .config import get_settings


@lru_cache
def get_neo4j_db():
    return GraphDatabase.driver(
        get_settings().database_url,
        auth=(get_settings().db_username, get_settings().db_password),
    )


DbClientDep = Annotated[Driver, Depends(get_neo4j_db)]
