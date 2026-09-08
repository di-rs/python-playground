from collections.abc import Generator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from psycopg import Connection
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from .config import get_settings


@lru_cache
def get_pg_pool():
    return ConnectionPool(
        conninfo=get_settings().database_url, kwargs={"row_factory": dict_row}
    )


def get_pg_client() -> Generator[Connection]:
    with get_pg_pool().connection() as conn:
        yield conn


PgClientDep = Annotated[Connection, Depends(get_pg_client)]
