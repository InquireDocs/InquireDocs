import logging

from fastapi import APIRouter, status, HTTPException

from app.schemas.summarizer import SummaryAvailableProvidersResponse, TextSummaryRequest
# from app.schemas.summarizer import PDFSummaryRequest, SummaryResponse
from app.schemas.summarizer import SummaryResponse
from app.core.summarizer import available_providers, get_summary_provider
from app.core.summarizer.summary_types import get_summary_types

# from app.models.schema import SummaryRequest
# from app.services.summarizer import get_summary_types, generate_summary


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/providers", response_model=SummaryAvailableProvidersResponse)
async def get_available_providers():
    """Get all available summarizer providers"""
    return {"providers": available_providers}


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
    try:
        # Get the provider
        summarizer = get_summary_provider(request.provider)

        # Generate the summary
        result = await summarizer.summarize_text(
            text=request.text,
            summary_type=request.summary_type,
            model=request.model,
            temperature=request.temperature,
            max_length=request.max_length
        )

        logger.error(result)

        return SummaryResponse(
            provider=result["provider"],
            summary_type=result["summary_type"],
            summary=result["summary"],
            model=result["model"],
            response_max_tokens=result["response_max_tokens"],
            source=result["source"],
            temperature=result["temperature"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}") from e


# @router.post("/pdf", response_model=SummaryResponse)
# async def summarize_pdf(request: PDFSummaryRequest):
    # file: UploadFile = File(...),
    # provider: str = Form(...),
    # model: Optional[str] = Form(None),
    # max_length: Optional[int] = Form(100)

    # provider: str = Form(..., description="Provider: openai or ollama"),
    #     summary_type: str = Field(..., description="Type of summary to generate"),
    #     model: Optional[str] = Form(None, description="Specific model to use (optional)"),
    #     max_length: Optional[int] = Form(100, description="Maximum length of the summary"),
    #     file: UploadFile = File(..., description="PDF file to summarise")

    # """Summarize a PDF document using the specified provider"""
    # pass
    # # Validate file type
    # if not request.file.filename.lower().endswith('.pdf'):
    #     raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # try:
    #     # Get the provider
    #     summarizer = get_summary_provider(request.provider)

    #     # Read file content
    #     file_content = await request.file.read()

    #     # Generate the summary
    #     result = await summarizer.summarize_pdf(
    #         file_content=file_content,
    #         file_name=request.file.filename,
    #         summary_type=request.summary_type,
    #         model=request.model,
    #         max_length=request.max_length
    #     )

    #     return SummaryResponse(
    #         provider=result["provider"],
    #         summary_type=request.summary_type,
    #         summary=result["summary"],
    #         model=result["model"],
    #         source=result["source"]
    #     )

    # except ValueError as e:
    #     raise HTTPException(status_code=400, detail=str(e)) from e

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"Error processing PDF: {str(e)}"
    #     ) from e

# @router.post("/summarize", status_code=status.HTTP_200_OK)
# def summarize(request: SummaryRequest):
#     """
#     Summarize a text provided in the request body.

#     Returns:
#         The summary of the text provided.
#     """
#     logger.debug("Summarize text")

#     try:
#         return generate_summary(request)
#     except (ValueError, Exception) as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error generating the summary.",
#         ) from e
