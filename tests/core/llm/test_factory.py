import pytest

from app.core.llm import get_llm_provider
from app.core.llm.openai import OpenAILLM
from app.core.llm.ollama import OllamaLLM


def test_get_openai_llm():
    """Test getting OpenAI LLM provider"""
    llm = get_llm_provider("openai")
    assert isinstance(llm, OpenAILLM)
    assert llm.provider_name == "openai"


def test_get_ollama_llm():
    """Test getting Ollama LLM provider"""
    llm = get_llm_provider("ollama")
    assert isinstance(llm, OllamaLLM)
    assert llm.provider_name == "ollama"


def test_get_unknown_llm():
    """Test getting an unknown LLM provider raises exception"""
    with pytest.raises(ValueError, match="Provider unknown not available or not configured"):
        get_llm_provider("unknown")
