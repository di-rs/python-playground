from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from redis import Redis

from .config import get_settings


@lru_cache
def get_redis_client():
    return Redis.from_url(
        get_settings().redis_url,
        decode_responses=True,
    )


RedisClientDep = Annotated[Redis, Depends(get_redis_client)]
