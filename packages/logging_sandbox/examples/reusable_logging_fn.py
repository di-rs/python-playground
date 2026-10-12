import logging

logger = logging.getLogger(__name__)


def log_payment_failed(
    *,
    payment_id: int,
    provider: str,
    reason: str,
) -> None:
    logger.warning(
        "Payment failed",
        extra={
            "event": "payment.failed",
            "payment_id": payment_id,
            "provider": provider,
            "reason": reason,
        },
        stacklevel=2,
    )


log_payment_failed(
    payment_id=32231,
    provider="paypal",
    reason="card_declined",
)
