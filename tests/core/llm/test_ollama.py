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
import pytest
from unittest.mock import patch, MagicMock

from app.core.llm.ollama import OllamaLLM
from app.core.config import settings


@pytest.fixture
def ollama_llm():
    """Fixture to create an OllamaLLM instance"""
    return OllamaLLM()


def test_ollama_initialization(ollama_llm):
    """Test OllamaLLM initialization"""
    assert ollama_llm.server_url == settings.ollama_base_url
    assert ollama_llm.provider_name == "ollama"


def test_get_embeddings_provider(ollama_llm):
    """Test getting embeddings provider"""
    with patch('app.core.llm.ollama.OllamaEmbeddings') as mock_embeddings:
        # Create a configuration to test
        ollama_llm.get_embeddings_provider()

        # Check if OllamaEmbeddings was initialized correctly
        mock_embeddings.assert_called_once_with(
            base_url=settings.ollama_base_url,
            model=settings.ollama_default_embeddings_model
        )

        # Test with a custom model
        custom_model = "custom-embedding-model"
        ollama_llm.get_embeddings_provider(model_name=custom_model)

        # Check if OllamaEmbeddings was initialized with the custom model
        mock_embeddings.assert_called_with(
            base_url=settings.ollama_base_url,
            model=custom_model
        )


@pytest.mark.asyncio
async def test_ask_with_default_parameters(ollama_llm):
    """Test ask method with default parameters"""
    query = "What is the meaning of life?"

    # Mock the ChatOllama class
    with patch('app.core.llm.ollama.ChatOllama') as mock_chat_ollama:
        # Create a mock for the response
        mock_response = MagicMock()
        mock_response.content = "The meaning of life is 42."
        mock_response.response_metadata = {"model": "llama2"}

        # Set up the mock to return our response
        chat_instance = mock_chat_ollama.return_value
        chat_instance.invoke.return_value = mock_response

        # Call the ask method
        result = await ollama_llm.ask(query)

        # Check if ChatOllama was initialized correctly
        mock_chat_ollama.assert_called_once_with(
            base_url=settings.ollama_base_url,
            model=settings.ollama_default_model,
            temperature=settings.default_model_temperature,
            num_predict=settings.default_max_tokens
        )

        # Check if invoke was called with the right parameters
        chat_instance.invoke.assert_called_once_with([("human", query)])

        # Check the returned response
        assert result["response"] == "The meaning of life is 42."
        assert result["model"] == "llama2"
        assert result["provider"] == "ollama"
        assert result["temperature"] == settings.default_model_temperature
        assert result["response_max_tokens"] == settings.default_max_tokens


@pytest.mark.asyncio
async def test_ask_with_custom_parameters(ollama_llm):
    """Test ask method with custom parameters"""
    query = "What is the meaning of life?"
    custom_model = "mistral"
    custom_temp = 0.2
    custom_max_tokens = 500

    # Mock the ChatOllama class
    with patch('app.core.llm.ollama.ChatOllama') as mock_chat_ollama:
        # Create a mock for the response
        mock_response = MagicMock()
        mock_response.content = "The meaning of life is 42."
        mock_response.response_metadata = {"model": custom_model}

        # Set up the mock to return our response
        chat_instance = mock_chat_ollama.return_value
        chat_instance.invoke.return_value = mock_response

        # Call the ask method with custom parameters
        result = await ollama_llm.ask(
            query,
            model=custom_model,
            temperature=custom_temp,
            max_tokens=custom_max_tokens
        )

        # Check if ChatOllama was initialized correctly with custom parameters
        mock_chat_ollama.assert_called_once_with(
            base_url=settings.ollama_base_url,
            model=custom_model,
            temperature=custom_temp,
            num_predict=custom_max_tokens
        )

        # Check the returned response
        assert result["model"] == custom_model
        assert result["temperature"] == custom_temp
        assert result["response_max_tokens"] == custom_max_tokens


@pytest.mark.asyncio
async def test_ask_exception_handling(ollama_llm):
    """Test exception handling in the ask method"""
    query = "What is the meaning of life?"

    # Mock the ChatOllama class to raise an exception
    with patch('app.core.llm.ollama.ChatOllama') as mock_chat_ollama:
        chat_instance = mock_chat_ollama.return_value
        chat_instance.invoke.side_effect = ValueError("Model not found")

        # Check if the method raises the expected exception
        with pytest.raises(ValueError, match="Error generating answer"):
            await ollama_llm.ask(query)
