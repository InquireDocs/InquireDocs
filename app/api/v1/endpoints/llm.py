import logging

from fastapi import APIRouter, HTTPException

from app.core.llm import get_llm_provider, available_providers
from app.schemas.llm import AvailableProvidersResponse, LLMRequest, LLMResponse


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/providers", response_model=AvailableProvidersResponse)
async def get_available_providers():
    """Get all available LLM providers"""
    return {"providers": available_providers}


@router.post("/ask", response_model=LLMResponse)
async def ask(request: LLMRequest):
    """Ask a question to the specified LLM provider"""
    try:
        # Get the provider
        llm_provider = get_llm_provider(request.provider)

        # Send the query
        result = await llm_provider.ask(
            query=request.query,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return LLMResponse(
            provider=result["provider"],
            response=result["response"],
            model=result["model"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}") from e
