import logging
import sys


class ColorFormatter(logging.Formatter):
    RESET = "\033[0m"
    DIM = "\033[2m"
    CYAN = "\033[36m"
    LEVEL_COLORS = {
        logging.DEBUG: "\033[34m",  # blue
        logging.INFO: "\033[32m",  # green
        logging.WARNING: "\033[33m",  # yellow
        logging.ERROR: "\033[31m",  # red
        logging.CRITICAL: "\033[1;31m",  # bold red
    }

    def format(self, record: logging.LogRecord) -> str:
        level_color = self.LEVEL_COLORS.get(record.levelno, "")

        time = self.formatTime(record, self.datefmt)
        message = record.getMessage()

        output = (
            f"{self.DIM}{time}{self.RESET} | "
            f"{level_color}{record.levelname:<8}{self.RESET} | "
            f"{self.CYAN}"
            f"{record.name}:{record.funcName}:{record.lineno}"
            f"{self.RESET} - "
            f"{message}"
        )

        # logging.exception(...) / exc_info=True
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

            output += f"\n{level_color}{record.exc_text}{self.RESET}"

        # stack_info=True
        if record.stack_info:
            output += f"\n{self.DIM}{record.stack_info}{self.RESET}"

        return output


def configure_logging(level: int = logging.DEBUG) -> None:
    logger = logging.getLogger("app")
    logger.setLevel(level)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(
        ColorFormatter(
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    logger.addHandler(console_handler)


configure_logging()


def run_very_cool_business_logic():
    logger = logging.getLogger("app")

    logger.debug("Debug message")
    logger.info("Application started")
    logger.warning("Something looks suspicious")
    logger.error("Something failed")
    logger.critical("Everything is on fire")

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("Failed to calculate value")


run_very_cool_business_logic()
