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

from fastapi import APIRouter, status, HTTPException, Depends

from app.core.config import settings
from app.core.summarizer import get_summary_provider
from app.core.summarizer.summary_types import get_summary_types
from app.schemas.summarizer import SummaryAvailableProvidersResponse, TextSummaryRequest
from app.schemas.summarizer import PDFSummaryRequest, SummaryResponse


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/providers", response_model=SummaryAvailableProvidersResponse)
async def get_available_providers():
    """Get all available summarizer providers"""
    return {"providers": settings.available_ai_providers}


@router.get("/types", status_code=status.HTTP_200_OK)
def summary_types():
    """Get the supported summary types"""
    logger.debug("Get summary types")
    try:
        return get_summary_types()
    except (ValueError, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting summary types.",
        ) from e


@router.post("/text", response_model=SummaryResponse)
async def summarize_text(request: TextSummaryRequest):
    """Summarize text using the specified provider"""
    logger.debug("Summarize text")
    try:
        # Get the provider
        summarizer = get_summary_provider(request.provider)

        # Generate the summary
        result = await summarizer.summarize_text(
            text=request.text,
            summary_type=request.summary_type,
            model=request.model,
            temperature=request.temperature,
            max_length=request.max_length,
        )

        return SummaryResponse(
            provider=result["provider"],
            summary_type=result["summary_type"],
            summary=result["summary"],
            model=result["model"],
            response_max_tokens=result["response_max_tokens"],
            source=result["source"],
            temperature=result["temperature"],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}") from e


@router.post("/pdf", response_model=SummaryResponse)
async def summarize_pdf(request: PDFSummaryRequest = Depends()):
    """Summarize a PDF file using the specified provider"""
    logger.debug("Summarize PDF document")

    # Validate file type
    if not request.file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Get the provider
        summarizer = get_summary_provider(request.provider)

        # Read file content
        file_content = await request.file.read()

        # Generate the summary
        result = await summarizer.summarize_pdf(
            file_content=file_content,
            file_name=request.file.filename,
            summary_type=request.summary_type,
            model=request.model,
            temperature=request.temperature,
            max_length=request.max_length,
        )

        return SummaryResponse(
            provider=result["provider"],
            summary_type=result["summary_type"],
            summary=result["summary"],
            model=result["model"],
            response_max_tokens=result["response_max_tokens"],
            source=result["source"],
            temperature=result["temperature"],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}") from e
