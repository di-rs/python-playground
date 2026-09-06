import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from ..dependencies import SessionDep

logger = logging.getLogger(__name__)

router = APIRouter(tags=["meta"])


@router.get("/health", response_model=None, status_code=status.HTTP_200_OK)
def healthcheck(session: SessionDep) -> dict[str, str] | JSONResponse:
    try:
        session.execute(text("SELECT 1"))
        logger.debug("Healthcheck requested")
        return {"status": "healthy"}
    except Exception:
        return JSONResponse(
            {"status": "unhealthy"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
