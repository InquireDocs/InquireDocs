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

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.core.config import settings
from app.core.llm.base import BaseLLM


logger = logging.getLogger(__name__)


class OpenAILLM(BaseLLM):
    """OpenAI LLM implementation"""

    def __init__(self):
        """Initialize OpenAI LLM from settings"""
        self.api_key = settings.openai_api_key

    @property
    def provider_name(self) -> str:
        return "openai"

    def get_embeddings_provider(self, model_name: Optional[str] = None) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            openai_api_key=self.api_key,
            model=model_name or settings.openai_default_embeddings_model,
        )

    async def ask(
        self,
        query: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Ask a question to OpenAI"""

        # Use default model if none provided
        model_name = model or settings.openai_default_model
        model_temperature = temperature or settings.default_model_temperature
        response_max_tokens = max_tokens or settings.default_max_tokens

        try:
            llm = ChatOpenAI(
                api_key=self.api_key,
                temperature=model_temperature,
                model_name=model_name,
                max_tokens=response_max_tokens,
            )

            return {
                "response": llm.invoke([("human", query)]),
                "model": model_name,
                "provider": self.provider_name,
                "temperature": model_temperature,
                "response_max_tokens": response_max_tokens,
            }
        except (ValueError, Exception) as e:
            msg = "Error generating answer"
            logger.error("%s: %s", msg, e)
            raise ValueError(msg) from e
