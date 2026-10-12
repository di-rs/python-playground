import logging

logger = logging.getLogger(__name__)


def make_greeting() -> str:
    logger.info("Running business logic")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Diving by zero!")
    return "World"
