import logging
import time

from fastapi import FastAPI, Request, status

from . import __version__
from .database import PgClientDep

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


@app.get("/board/{board_id}", status_code=status.HTTP_200_OK)
def get_board(client: PgClientDep, board_id: int):
    comments = client.execute(
        t"""SELECT * FROM comments
        NATURAL LEFT JOIN rich_content
        WHERE board_id = {board_id}
        """
    ).fetchmany()

    board = client.execute(
        t"SELECT * FROM boards WHERE board_id = {board_id}"
    ).fetchone()

    return {"comments": comments, "board": board or {}}
