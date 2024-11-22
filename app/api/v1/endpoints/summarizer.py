import logging

from fastapi import APIRouter, status, HTTPException

from app.models.schema import SummaryRequest
from app.services.summarizer import get_summary_types, generate_summary


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/summary_types", status_code=status.HTTP_200_OK)
def summary_types():
    """Get the supported summary types"""
    logger.debug("Get summary types")
    try:
        return get_summary_types()
    except (ValueError, Exception) as e:
        raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="Error getting summary types."
        ) from e


@router.post("/summarize", status_code=status.HTTP_200_OK)
def summarize(request: SummaryRequest):
    """
    Summarize a text provided in the request body.

    Returns:
        The summary of the text provided.
    """
    logger.debug("Summarize text")

    try:
        return generate_summary(request)
    except (ValueError, Exception) as e:
        raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail="Error generating the summary."
        ) from e
