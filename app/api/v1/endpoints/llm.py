#  Copyright 2024-present Julian Nonino
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.llm import get_llm_provider
from app.schemas.llm import LLMAvailableProvidersResponse, LLMRequest, LLMResponse


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/providers", response_model=LLMAvailableProvidersResponse)
async def get_available_providers():
    """Get all available LLM providers"""
    return {"providers": settings.available_ai_providers}


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
            model=result["model"],
            temperature=result["temperature"],
            response_max_tokens=result["response_max_tokens"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}") from e
