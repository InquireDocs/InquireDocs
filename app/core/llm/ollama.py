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

    @property
    def provider_name(self) -> str:
        return "ollama"

    def get_embeddings_provider(self, model_name: Optional[str] = None) -> OllamaEmbeddings:
        """Return the embeddings model"""
        return OllamaEmbeddings(
            base_url=self.server_url, model=model_name or settings.ollama_default_embeddings_model
        )

    async def ask(
        self,
        query: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Ask a question to OpenAI"""

        # Use default values if none custom provided
        model_name = model or settings.ollama_default_model
        model_temperature = temperature or settings.default_model_temperature
        response_max_tokens = max_tokens or settings.default_max_tokens

        try:
            llm = ChatOllama(
                base_url=self.server_url,
                model=model_name,
                temperature=model_temperature,
                num_predict=response_max_tokens,
            )

            answer = llm.invoke([("human", query)])
            logger.info(answer)

            return {
                "response": answer.content,
                "model": answer.response_metadata["model"],
                "provider": self.provider_name,
                "temperature": model_temperature,
                "response_max_tokens": response_max_tokens,
            }
        except (ValueError, Exception) as e:
            msg = "Error generating answer"
            logger.error("%s: %s", msg, e)
            raise ValueError(msg) from e
