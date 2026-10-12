import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

# handler = logging.FileHandler("app.log")

handler = RotatingFileHandler(
    filename="app.log",
    maxBytes=1 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8",
)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
)

timed_handler = TimedRotatingFileHandler(
    filename="app.log",
    when="midnight",
    interval=1,
    backupCount=14,
    encoding="utf-8",
    utc=True,
)
timed_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(timed_handler)


logger.debug("Creating an order", extra={"user_id": "23232"})
logger.info("Order was created", extra={"user_id": "23232"})
logger.warning("Order creation API is not responding, retrying...")
logger.error("Order creation API is not responding, 3 retries didn't help")
logger.critical("System config error, shutting down")
