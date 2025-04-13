# import httpx
import logging
# import os
# import tempfile
from typing import Optional, Dict, Any

# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama

from app.core.config import settings
from app.core.summarizer.base import BaseSummarizer


logger = logging.getLogger(__name__)


class OllamaSummarizer(BaseSummarizer):
    """Ollama summarizer implementation"""

    def __init__(self):
        """Initialize Ollama with base URL from settings"""
        self.server_url = settings.ollama_base_url

    @property
    def provider_name(self) -> str:
        return "ollama"

    async def summarize_text(
        self,
        text: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = settings.ollama_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: Optional[int] = settings.default_model_temperature,
    ) -> Dict[str, Any]:
        """Summarize text using Ollama"""
        try:
            # Prepare LLM
            llm = ChatOllama(
                base_url=self.server_url,
                model=model,
                temperature=temperature,
                num_predict=max_length
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
        model: Optional[str] = settings.ollama_default_model,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: Optional[int] = settings.default_model_temperature,
    ) -> Dict[str, Any]:
        """Summarize PDF using Ollama"""
        try:
            # Prepare LLM
            llm = ChatOllama(
                base_url=self.server_url,
                model=model,
                temperature=temperature,
                num_predict=max_length
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
