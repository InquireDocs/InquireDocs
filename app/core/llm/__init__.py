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
from typing import Dict, Type

from app.core.config import settings
from app.core.llm.base import BaseLLM
from app.core.llm.openai import OpenAILLM
from app.core.llm.ollama import OllamaLLM

# Factory for LLM providers
_llm_providers: Dict[str, Type[BaseLLM]] = {
    "ollama": OllamaLLM,
    "openai": OpenAILLM,
}


def get_llm_provider(provider: str) -> BaseLLM:
    """
    Get an LLM provider instance by name

    Args:
        provider: The name of the provider

    Returns:
        An instance of the LLM provider

    Raises:
        ValueError: If the provider is not available or not supported
    """
    available_providers = settings.available_ai_providers

    if provider not in available_providers:
        raise ValueError(f"Provider {provider} not available or not configured")

    if provider not in _llm_providers:
        raise ValueError(f"Provider {provider} not supported")

    return _llm_providers[provider]()
