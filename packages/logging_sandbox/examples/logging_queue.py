import logging
import queue
import sys
from logging.handlers import QueueHandler, QueueListener

log_queue = queue.SimpleQueue()

queue_handler = QueueHandler(log_queue)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
)

listener = QueueListener(
    log_queue,
    stream_handler,
    respect_handler_level=True,
)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(queue_handler)

listener.start()

try:
    logger = logging.getLogger(__name__)
    logger.info("HALLLOOOOOOOO!")
    logger.warning("Somsing is happennign!")
finally:
    listener.stop()
