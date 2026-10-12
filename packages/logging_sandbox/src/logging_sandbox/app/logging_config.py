import copy
import json
import logging
import os
from contextvars import ContextVar
from datetime import UTC, datetime

request_id_var = ContextVar("request_id", default="-")

SERVICE_NAME = "fastapi-logging-demo"
ENVIRONMENT = os.getenv("APP_ENV", "dev")


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
            "service": SERVICE_NAME,
            "environment": ENVIRONMENT,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.addFilter(RequestContextFilter())
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    for name in ("uvicorn", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(name)

        for uvicorn_handler in tuple(uvicorn_logger.handlers):
            uvicorn_logger.removeHandler(uvicorn_handler)

        uvicorn_logger.propagate = True
