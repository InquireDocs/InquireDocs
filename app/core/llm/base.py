# Copyright 2025 Julian Nonino
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from langchain_core.embeddings import Embeddings


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
        temperature: Optional[float] = None,
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
