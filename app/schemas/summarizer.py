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
from typing import List, Optional

from fastapi import UploadFile, File
from pydantic import BaseModel, Field

from app.core.config import settings


class SummaryAvailableProvidersResponse(BaseModel):
    providers: List[str]


class TextSummaryRequest(BaseModel):
    provider: str = Field("ollama", description="Provider: openai or ollama")
    text: str = Field(..., description="Text to summarize")
    summary_type: str = Field(
        settings.default_summary_type, description="Type of summary to generate (optional)"
    )
    model: Optional[str] = Field(
        settings.ollama_default_model, description="Specific model to use (optional)"
    )
    temperature: Optional[float] = Field(
        settings.default_model_temperature, description="Model temperature to use (optional)"
    )
    max_length: Optional[int] = Field(
        settings.default_max_tokens, description="Maximum summary length (optional)"
    )

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "provider": "ollama",
                "summary_type": "concise",
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit...",
                "model": settings.ollama_default_model,
                "max_length": settings.default_max_tokens,
            }
        }


class PDFSummaryRequest(BaseModel):
    provider: str = Field("ollama", description="Provider: openai or ollama")
    file: UploadFile = File(..., description="PDF file to summarise")
    summary_type: str = Field(
        settings.default_summary_type, description="Type of summary to generate (optional)"
    )
    model: Optional[str] = Field(
        settings.ollama_default_model, description="Specific model to use (optional)"
    )
    temperature: Optional[float] = Field(
        settings.default_model_temperature, description="Model temperature to use (optional)"
    )
    max_length: Optional[int] = Field(
        settings.default_max_tokens, description="Maximum summary length (optional)"
    )


class SummaryResponse(BaseModel):
    model: Optional[str] = None
    provider: str
    response_max_tokens: int
    summary: str
    summary_type: str
    source: str = Field("text", description="Source of the original content (text or pdf)")
    temperature: float
