import logging
import time
from datetime import UTC, datetime

from fastapi import FastAPI, Request, status

from redix.database import RedisClientDep

from . import __version__

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Databases Sandbox API",
    version=__version__,
    description="An API for tracking project milestones and tasks for devs.",
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s completed in %.2fms with status code %s",
        request.method,
        request.url.path,
        process_time,
        response.status_code,
    )
    return response


@app.get("/pageview", status_code=status.HTTP_200_OK)
def pageview(client: RedisClientDep):
    views = client.incr("pageviews")
    return {"views": views}


def very_slow_expensive_function() -> str:
    logger.info("oh no, expensive call!")
    time.sleep(10)
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@app.get("/get", status_code=status.HTTP_200_OK)
def root(client: RedisClientDep):
    key = "very_slow_expensive_function"
    data = client.get(key)

    if data is None:
        data = very_slow_expensive_function()
        client.set(key, data, ex=10)

    return {"data": data}
