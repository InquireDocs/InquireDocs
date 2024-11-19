import pytest
from unittest.mock import patch, MagicMock
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from pydantic import SecretStr


from app.services.llm import (
    get_ollama_embeddings_model,
    get_ollama_model,
    get_openai_embeddings_model,
    get_openai_model
)

# Test constants
TEST_SERVER_URL = "http://localhost:11434"
TEST_OLLAMA_MODEL = "llama3"
TEST_OPENAI_MODEL = "gpt-4o"
TEST_API_KEY = "test-api-key"
TEST_TEMPERATURE = 0.7


def test_get_ollama_embeddings_model_success():
    """Test successful creation of Ollama embeddings model"""
    ollama_embeddings = get_ollama_embeddings_model(
        server_url=TEST_SERVER_URL,
        embeddings_model=TEST_OLLAMA_MODEL
    )

    assert isinstance(ollama_embeddings, OllamaEmbeddings)
    assert ollama_embeddings.base_url == TEST_SERVER_URL
    assert ollama_embeddings.model == TEST_OLLAMA_MODEL


def test_get_ollama_model_success():
    """Test successful creation of Ollama language model"""
    ollama_model = get_ollama_model(
        server_url=TEST_SERVER_URL,
        ai_model=TEST_OLLAMA_MODEL
    )

    assert isinstance(ollama_model, OllamaLLM)
    assert ollama_model.base_url == TEST_SERVER_URL
    assert ollama_model.model == TEST_OLLAMA_MODEL


def test_get_openai_embeddings_model_success():
    """Test successful creation of OpenAI embeddings model"""
    openai_embeddings = get_openai_embeddings_model(
        api_key=TEST_API_KEY,
        embeddings_model=TEST_OPENAI_MODEL
    )

    assert isinstance(openai_embeddings, OpenAIEmbeddings)
    assert openai_embeddings.openai_api_key == SecretStr(TEST_API_KEY)
    assert openai_embeddings.model == TEST_OPENAI_MODEL


def test_get_openai_model_success():
    """Test successful creation of OpenAI chat model"""
    openai_model = get_openai_model(
        api_key=TEST_API_KEY,
        model=TEST_OPENAI_MODEL,
        model_temperature=TEST_TEMPERATURE
    )

    assert isinstance(openai_model, ChatOpenAI)
    assert openai_model.openai_api_key == SecretStr(TEST_API_KEY)
    assert openai_model.model_name == TEST_OPENAI_MODEL
    assert openai_model.temperature == TEST_TEMPERATURE
