import json
import logging
from datetime import UTC, datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=UTC
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "user_id": getattr(record, "user_id", None)
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

logger.debug("Creating an order",  extra={"user_id": "23232"})
logger.info("Order was created", extra={"user_id": "23232"})
logger.warning("Order creation API is not responding, retrying...")
logger.error("Order creation API is not responding, 3 retries didn't help")
logger.critical("System config error, shutting down")
