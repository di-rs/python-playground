import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class SensitiveDataFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        message = re.sub(
            r"(password|token)=\S+",
            r"\1=***",
            message,
            flags=re.IGNORECASE,
        )
        return message


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    SensitiveDataFormatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
logger.addHandler(handler)

logger.debug("Creating an order")
logger.info("Order was created token=dsdssdj236vbds")
logger.warning("Order creation API is not responding, retrying...")
logger.error("Order creation API is not responding, 3 retries didn't help")
logger.critical("System config error, shutting down")
