from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from langchain_core.embeddings import Embeddings
# from langchain_core.language_models.chat_models import BaseChatModel


class BaseLLM(ABC):
    """Base class for LLM providers"""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name"""
        pass

    @abstractmethod
    def get_embeddings_provider(
        self,
        model_name: Optional[str] = None
    ) -> Embeddings:
        pass

    @abstractmethod
    async def ask(
        self,
        query: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Ask a question to the LLM

        Args:
            query: The question to ask
            model: Specific model to use
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary containing the response and metadata
        """
        pass
