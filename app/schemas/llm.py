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

from pydantic import BaseModel, Field


class LLMAvailableProvidersResponse(BaseModel):
    providers: List[str]


class LLMRequest(BaseModel):
    provider: str = Field(..., description="LLM provider: openai or ollama")
    query: str = Field(..., description="The question to ask the LLM")
    model: Optional[str] = Field(None, description="Specific model to use (optional)")
    temperature: Optional[float] = Field(0.7, description="Temperature for generation")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "provider": "openai",
                "query": "What is the capital of France?",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 100,
            }
        }


class LLMResponse(BaseModel):
    provider: str
    response: str
    model: Optional[str] = None
    temperature: float
    response_max_tokens: int
