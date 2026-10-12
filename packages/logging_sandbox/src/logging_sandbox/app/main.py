import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request

from .logging_config import configure_logging, request_id_var
from .services.greeting import make_greeting

configure_logging()
logger = logging.getLogger(__name__)
app = FastAPI()


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = uuid4().hex
    token = request_id_var.set(request_id)
    started_at = perf_counter()

    try:
        logger.info("Request started: %s %s", request.method, request.url.path)
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Unhandled exception occured: duration_ms=%.1f",
            duration_ms,
        )
        raise
    else:
        duration_ms = (perf_counter() - started_at) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "Request has finished: status=%s duration_ms=%.1f",
            response.status_code,
            duration_ms,
        )
        return response
    finally:
        request_id_var.reset(token)


@app.get("/")
def read_root():
    logger.info("Enter / endpoint")
    return {"Hello": make_greeting()}
