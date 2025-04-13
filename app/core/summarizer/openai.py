import logging
from typing import Optional, Dict, Any

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.core.summarizer.base import BaseSummarizer


logger = logging.getLogger(__name__)


class OpenAISummarizer(BaseSummarizer):
    """OpenAI summarizer implementation"""

    def __init__(self):
        """Initialize OpenAI client with API key from settings"""
        self.api_key = settings.openai_api_key
        self.default_model = settings.openai_default_model

    @property
    def provider_name(self) -> str:
        return "openai"

    async def summarize_text(
        self,
        text: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = settings.openai_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: int = settings.default_max_tokens,
    ) -> Dict[str, Any]:
        """Summarize text using OpenAI"""
        try:
            # Prepare LLM
            llm = ChatOpenAI(
                api_key=self.api_key,
                temperature=temperature,
                model_name=model,
                max_tokens=max_length
            )

            generated_summary = await self.generate_text_summary(summary_type, llm, text)

            return {
                "model": model,
                "provider": self.provider_name,
                "response_max_tokens": max_length,
                "summary": generated_summary,
                "summary_type": summary_type,
                "source": "text",
                "temperature": temperature
            }
        except (ValueError, Exception) as e:
            msg = "Error summarizing text"
            logger.error("%s: %s", msg, e)
            raise ValueError(msg) from e

    async def summarize_pdf(
        self,
        file_content: bytes,
        file_name: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = settings.openai_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: int = settings.default_max_tokens,
    ) -> Dict[str, Any]:
        """Summarize PDF using OpenAI"""
        try:
            # Prepare LLM
            llm = ChatOpenAI(
                api_key=self.api_key,
                temperature=temperature,
                model_name=model,
                max_tokens=max_length
            )

            generated_summary = await self.generate_pdf_summary(
                summary_type=summary_type,
                llm=llm,
                file_content=file_content
            )

            return {
                "model": model,
                "provider": self.provider_name,
                "response_max_tokens": max_length,
                "summary": generated_summary,
                "summary_type": summary_type,
                "source": "pdf",
                "temperature": temperature
            }
        except (ValueError, Exception) as e:
            msg = "Error summarizing PDF document"
            logger.error("%s: %s", msg, e)
            raise ValueError(msg) from e
