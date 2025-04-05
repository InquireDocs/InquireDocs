from typing import Dict, Type

from app.core.llm.base import BaseLLM
from app.core.llm.openai import OpenAILLM
from app.core.llm.ollama import OllamaLLM
from app.core.config import settings

# Factory for LLM providers
_llm_providers: Dict[str, Type[BaseLLM]] = {
    "openai": OpenAILLM,
    "ollama": OllamaLLM,
}

# Available providers based on config
available_providers = settings.available_llm_providers


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
    if provider not in available_providers:
        raise ValueError(f"Provider {provider} not available or not configured")

    if provider not in _llm_providers:
        raise ValueError(f"Provider {provider} not supported")

    return _llm_providers[provider]()
