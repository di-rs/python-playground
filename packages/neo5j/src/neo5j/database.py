from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from neo4j import GraphDatabase
from neo4j._sync.driver import Driver

from .config import get_settings


def get_neo4j_db():
    return GraphDatabase.driver(
        get_settings().database_url,
        auth=(get_settings().db_username, get_settings().db_password),
    )


def get_neo4j_client() -> Generator[Driver]:
    with get_neo4j_db() as driver:
        yield driver


DbClientDep = Annotated[Driver, Depends(get_neo4j_client)]
