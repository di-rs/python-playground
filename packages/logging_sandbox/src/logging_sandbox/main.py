import copy
import json
import logging
from contextvars import ContextVar
from datetime import UTC, datetime
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request

request_id_var = ContextVar("request_id", default="-")


class RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> logging.LogRecord:
        record = copy.copy(record)
        record.request_id = request_id_var.get()
        return record


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(
                record.created, UTC
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


handler = logging.StreamHandler()
handler.addFilter(RequestContextFilter())
handler.setFormatter(JsonFormatter())

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

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


def business_logic() -> str:
    logger.info("Running business logic")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Diving by zero!")
    return "World"


@app.get("/")
def read_root():
    logger.info("Enter / endpoint")
    return {"Hello": business_logic()}
