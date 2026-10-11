import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s, %(user_id)s: %(message)s",
        defaults={"user_id": "-"},
    )
)
logger.addHandler(handler)

logger.debug("Creating an order",  extra={"user_id": "23232"})
logger.info("Order was created", extra={"user_id": "23232"})
logger.warning("Order creation API is not responding, retrying...")
logger.error("Order creation API is not responding, 3 retries didn't help")
logger.critical("System config error, shutting down")
