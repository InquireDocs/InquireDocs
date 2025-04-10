from abc import ABC, abstractmethod
import logging
from typing import Optional, Dict, Any

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel

from app.core.config import settings
from app.core.summarizer.summary_types import get_summary_type_details


logger = logging.getLogger(__name__)


class BaseSummarizer(ABC):
    """Base class for summarizer providers"""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name"""
        pass

    @abstractmethod
    async def summarize_text(
        self,
        text: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = None,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: int = settings.default_max_tokens
    ) -> Dict[str, Any]:
        """
        Summarize a text

        Args:
            text: The text to summarize
            summary_type: They type of summary to generate
            model: Specific model to use
            temperature: Temperature for generation
            max_length: Maximum length of the summary

        Returns:
            Dictionary containing the summary and metadata
        """
        pass

    @abstractmethod
    async def summarize_pdf(
        self,
        file_content: bytes,
        file_name: str,
        summary_type: Optional[str] = settings.default_summary_type,
        model: Optional[str] = None,
        temperature: Optional[float] = settings.default_model_temperature,
        max_length: int = settings.default_max_tokens
    ) -> Dict[str, Any]:
        """
        Summarize a PDF document

        Args:
            file_content: The binary content of the PDF file
            file_name: Name of the original file
            summary_type: They type of summary to generate
            model: Specific model to use
            temperature: Temperature for generation
            max_length: Maximum length of the summary

        Returns:
            Dictionary containing the summary and metadata
        """
        pass

    async def generate_text_summary(self, summary_type: str, llm: BaseChatModel, text: str) -> str:
        try:
            # Define prompt
            summary_type_details = get_summary_type_details(summary_type)
            prompt_template = summary_type_details.get("prompt")
            prompt = PromptTemplate.from_template(prompt_template)

            # Define StuffDocumentsChain
            stuff_chain = create_stuff_documents_chain(llm, prompt)

            # Run summarize on the text
            docs = [Document(page_content=text)]
            return stuff_chain.invoke({"context": docs})
        except (ValueError, Exception) as e:
            msg = "Error generating text summary"
            logger.error("%s: %s", msg, e)
            raise ValueError(msg) from e
