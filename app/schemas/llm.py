from pydantic import BaseModel, Field
from typing import List, Optional


class LLMRequest(BaseModel):
    provider: str = Field(..., description="LLM provider: openai, anthropic, or ollama")
    query: str = Field(..., description="The question to ask the LLM")
    model: Optional[str] = Field(None, description="Specific model to use (optional)")
    temperature: Optional[float] = Field(0.7, description="Temperature for generation")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")

    class Config:
        json_schema_extra = {
            "example": {
                "provider": "openai",
                "query": "What is the capital of France?",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 100
            }
        }


class LLMResponse(BaseModel):
    provider: str
    response: str
    model: Optional[str] = None


class AvailableProvidersResponse(BaseModel):
    providers: List[str]
