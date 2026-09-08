from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pymongo import MongoClient

from .config import get_settings


@lru_cache
def get_mongo_client() -> MongoClient:
    return MongoClient(get_settings().mongo_url)


MongoClientDep = Annotated[MongoClient, Depends(get_mongo_client)]
