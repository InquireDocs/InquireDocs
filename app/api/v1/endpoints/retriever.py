import logging

from fastapi import APIRouter, status, HTTPException

from app.models.schema import QuestionRequest
from app.services.retriever import get_answer


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/ask", status_code=status.HTTP_200_OK)
def summarize(request: QuestionRequest):
    """
    Gets an answer from an LLM to the question received.

    Returns:
        The answer to the question asked.
    """
    logger.debug("Answer question")

    try:
        return get_answer(request)
    except (ValueError, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error answering the question.",
        ) from e
