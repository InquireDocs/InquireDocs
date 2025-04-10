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

available_providers = settings.available_ai_providers


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
    if provider not in available_providers:
        raise ValueError(f"Provider {provider} not available or not configured")

    if provider not in _summary_providers:
        raise ValueError(f"Provider {provider} not supported")

    return _summary_providers[provider]()
