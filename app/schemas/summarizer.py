from typing import List, Optional

from fastapi import UploadFile, File, Form
from pydantic import BaseModel, Field

from app.core.config import settings


class SummaryAvailableProvidersResponse(BaseModel):
    providers: List[str]


class TextSummaryRequest(BaseModel):
    provider: str = Field(..., description="Provider: openai or ollama")
    text: str = Field(..., description="Text to summarize")
    summary_type: str = Field(
        settings.default_summary_type,
        description="Type of summary to generate (optional)"
    )
    model: Optional[str] = Field("ollama", description="Specific model to use (optional)")
    temperature: Optional[float] = Field(
        settings.default_model_temperature,
        description="Model temperature to use (optional)"
    )
    max_length: Optional[int] = Field(
        settings.default_max_tokens,
        description="Maximum summary length (optional)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "provider": "ollama",
                "summary_type": "concise",
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
                "model": settings.ollama_default_model,
                "max_length": settings.default_max_tokens
            }
        }


class PDFSummaryRequest:
    def __init__(
        self,
        provider: str = Form(..., description="Provider: openai or ollama"),
        summary_type: str = Field(..., description="Type of summary to generate"),
        model: Optional[str] = Form(None, description="Specific model to use (optional)"),
        max_length: Optional[int] = Form(100, description="Maximum length of the summary"),
        file: UploadFile = File(..., description="PDF file to summarise")
    ):
        self.provider = provider
        self.summary_type = summary_type
        self.model = model
        self.max_length = max_length
        self.file = file


class SummaryResponse(BaseModel):
    model: Optional[str] = None
    provider: str
    response_max_tokens: int
    summary: str
    summary_type: str
    source: str = Field("text", description="Source of the original content (text or pdf)")
    temperature: float
