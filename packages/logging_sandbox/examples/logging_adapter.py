import logging

order_id = 1337

logger = logging.getLogger(__name__)
order_logger = logging.LoggerAdapter(
    logger,
    {"order_id": order_id},
)

order_logger.info("Starting order process")
order_logger.info("Payment was done")
order_logger.info("Order processed")
