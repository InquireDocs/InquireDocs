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
from app.core.summarizer.base import BaseSummarizer
from app.core.summarizer.ollama import OllamaSummarizer
from app.core.summarizer.openai import OpenAISummarizer


# Factory for Summary providers
_summary_providers: Dict[str, Type[BaseSummarizer]] = {
    "ollama": OllamaSummarizer,
    "openai": OpenAISummarizer,
}


def get_summary_provider(provider: str) -> BaseSummarizer:
    """
    Get an Summary provider instance by name

    Args:
        provider: The name of the provider

    Returns:
        An instance of the Summary provider

    Raises:
        ValueError: If the provider is not available or not supported
    """
    available_providers = settings.available_ai_providers

    if provider not in available_providers:
        raise ValueError(f"Provider {provider} not available or not configured")

    if provider not in _summary_providers:
        raise ValueError(f"Provider {provider} not supported")

    return _summary_providers[provider]()
