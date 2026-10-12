import copy
import logging
import sys


def get_user_id() -> int | None:
    return 123


class UserContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> logging.LogRecord:
        record = copy.copy(record)
        record.user_id = get_user_id()
        return record


class InfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == logging.INFO or record.levelno == logging.ERROR


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s user_id=%(user_id)s: %(message)s",
        defaults={"user_id": "-"},
    )
)
stream_handler.addFilter(InfoFilter())
stream_handler.addFilter(UserContextFilter())

logger.addHandler(stream_handler)

logger.debug("Creating an order")
logger.info("Order was created")
logger.warning("Order creation API is not responding, retrying...")
logger.error("Order creation API is not responding, 3 retries didn't help")
logger.critical("System config error, shutting down")
