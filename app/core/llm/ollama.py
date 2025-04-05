import logging
from typing import Optional, Dict, Any

from langchain_ollama import ChatOllama, OllamaEmbeddings

from app.core.config import settings
from app.core.llm.base import BaseLLM


logger = logging.getLogger(__name__)


class OllamaLLM(BaseLLM):
    """Ollama LLM implementation"""

    def __init__(self):
        """Initialize Ollama LLM from settings"""
        self.server_url = settings.ollama_base_url
        self.default_embeddings_model = settings.ollama_default_embeddings_model
        self.default_chat_model = settings.ollama_default_model
        self.default_model_temperature = settings.default_model_temperature
        self.default_max_tokens = settings.default_max_tokens

    @property
    def provider_name(self) -> str:
        return "ollama"

    def get_embeddings_provider(self, model_name: Optional[str] = None) -> OllamaEmbeddings:
        """Return the embeddings model"""
        return OllamaEmbeddings(
            base_url=self.server_url,
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

        # Use default values if none custom provided
        model_name = model or self.default_chat_model
        model_temperature = temperature or self.default_model_temperature
        response_max_tokens = max_tokens or self.default_max_tokens

        try:
            llm = ChatOllama(
                base_url=self.server_url,
                model=model_name,
                temperature=model_temperature,
                num_predict=response_max_tokens
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
