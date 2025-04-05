import logging
from typing import Optional, Dict, Any

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core.config import settings
from app.core.llm.base import BaseLLM


logger = logging.getLogger(__name__)


class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation"""

    def __init__(self):
        """Initialize OpenAI LLM from settings"""
        self.api_key = settings.openai_api_key
        self.default_embeddings_model = settings.openai_default_embeddings_model
        self.default_chat_model = settings.openai_default_model
        self.default_model_temperature = settings.default_model_temperature
        self.default_max_tokens = settings.default_max_tokens

    @property
    def provider_name(self) -> str:
        return "openai"

    def get_embeddings_provider(self, model_name: Optional[str] = None) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            openai_api_key=self.api_key,
            model=model_name or self.default_embeddings_model
        )

    async def ask(
        self,
        query: str,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Ask a question to OpenAI"""

        # Use default model if none provided
        model_name = model or self.default_chat_model
        model_temperature = temperature or self.default_model_temperature
        response_max_tokens = max_tokens or self.default_max_tokens

        try:
            llm = ChatOpenAI(
                api_key=self.api_key,
                temperature=model_temperature,
                model_name=model_name,
                max_tokens=response_max_tokens
            )

            return {
                "response": llm.invoke([("human", query)]),
                "model": model_name,
                "provider": self.provider_name
            }
        except (ValueError, Exception) as e:
            msg = "Error generating answer"
            logger.error("%s: %s", msg, e)
            raise ValueError(msg) from e
