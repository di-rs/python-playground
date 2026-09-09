import logging
import time

from fastapi import FastAPI, Request, status

from neo5j.database import DbClientDep

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


@app.get("/get-path", status_code=status.HTTP_200_OK)
def root(client: DbClientDep, person1: str, person2: str):
    res = client.execute_query(
        """
        MATCH path = shortestPath(
            (First:Person {name: $person1 })
            -[*]-
            (Second:Person {name: $person2 })
        )
        UNWIND nodes(path) as node
        RETURN coalesce(node.name, node.title) as text;
    """,
        person1=person1,
        person2=person2,
    )

    return {"path": [record.get("text") for record in res.records]}
