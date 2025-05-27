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
from unittest.mock import patch

from app.core.llm.openai import OpenAILLM
from app.core.config import settings


@pytest.fixture
def openai_llm():
    """Fixture to create an OpenAILLM instance"""
    return OpenAILLM()


def test_openai_initialization(openai_llm):
    """Test OpenAILLM initialization"""
    assert openai_llm.api_key == settings.openai_api_key
    assert openai_llm.provider_name == "openai"


def test_get_embeddings_provider(openai_llm):
    """Test getting embeddings provider"""
    with patch('app.core.llm.openai.OpenAIEmbeddings') as mock_embeddings:
        # Create a configuration to test
        openai_llm.get_embeddings_provider()

        # Check if OpenAIEmbeddings was initialized correctly
        mock_embeddings.assert_called_once_with(
            openai_api_key=settings.openai_api_key,
            model=settings.openai_default_embeddings_model
        )

        # Test with a custom model
        custom_model = "text-embedding-3-large"
        openai_llm.get_embeddings_provider(model_name=custom_model)

        # Check if OpenAIEmbeddings was initialized with the custom model
        mock_embeddings.assert_called_with(
            openai_api_key=settings.openai_api_key,
            model=custom_model
        )


@pytest.mark.asyncio
async def test_ask_with_default_parameters(openai_llm):
    """Test ask method with default parameters"""
    query = "What is the meaning of life?"

    # Mock the ChatOpenAI class
    with patch('app.core.llm.openai.ChatOpenAI') as mock_chat_openai:
        # Create a mock for the response
        mock_response = "The meaning of life is 42."

        # Set up the mock to return our response
        chat_instance = mock_chat_openai.return_value
        chat_instance.invoke.return_value = mock_response

        # Call the ask method
        result = await openai_llm.ask(query)

        # Check if ChatOpenAI was initialized correctly
        mock_chat_openai.assert_called_once_with(
            api_key=settings.openai_api_key,
            temperature=settings.default_model_temperature,
            model_name=settings.openai_default_model,
            max_tokens=settings.default_max_tokens
        )

        # Check if invoke was called with the right parameters
        chat_instance.invoke.assert_called_once_with([("human", query)])

        # Check the returned response
        assert result["response"] == mock_response
        assert result["model"] == settings.openai_default_model
        assert result["provider"] == "openai"
        assert result["temperature"] == settings.default_model_temperature
        assert result["response_max_tokens"] == settings.default_max_tokens


@pytest.mark.asyncio
async def test_ask_with_custom_parameters(openai_llm):
    """Test ask method with custom parameters"""
    query = "What is the meaning of life?"
    custom_model = "gpt-4o"
    custom_temp = 0.2
    custom_max_tokens = 500

    # Mock the ChatOpenAI class
    with patch('app.core.llm.openai.ChatOpenAI') as mock_chat_openai:
        # Create a mock for the response
        mock_response = "The meaning of life is 42."

        # Set up the mock to return our response
        chat_instance = mock_chat_openai.return_value
        chat_instance.invoke.return_value = mock_response

        # Call the ask method with custom parameters
        result = await openai_llm.ask(
            query,
            model=custom_model,
            temperature=custom_temp,
            max_tokens=custom_max_tokens
        )

        # Check if ChatOpenAI was initialized correctly with custom parameters
        mock_chat_openai.assert_called_once_with(
            api_key=settings.openai_api_key,
            temperature=custom_temp,
            model_name=custom_model,
            max_tokens=custom_max_tokens
        )

        # Check the returned response
        assert result["model"] == custom_model
        assert result["temperature"] == custom_temp
        assert result["response_max_tokens"] == custom_max_tokens


@pytest.mark.asyncio
async def test_ask_exception_handling(openai_llm):
    """Test exception handling in the ask method"""
    query = "What is the meaning of life?"

    # Mock the ChatOpenAI class to raise an exception
    with patch('app.core.llm.openai.ChatOpenAI') as mock_chat_openai:
        chat_instance = mock_chat_openai.return_value
        chat_instance.invoke.side_effect = ValueError("API key not valid")

        # Check if the method raises the expected exception
        with pytest.raises(ValueError, match="Error generating answer"):
            await openai_llm.ask(query)
