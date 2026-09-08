import logging
import time

from fastapi import FastAPI, Request, status
from pymongo import TEXT

from mongo.database import MongoClientDep

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


@app.get("/pets", status_code=status.HTTP_200_OK)
def list_pets(client: MongoClientDep, search: str):
    db = client.get_database("adoption")
    collection = db["pets"]

    collection.create_index([("name", TEXT)])

    pets = (
        collection.find(
            {
                "$text": {"$search": search},
            },
            {"_id": False},
        )
        .sort([("score", {"$meta": "textScore"})])
        .limit(10)
        .to_list()
    )

    return {"pets": pets}
