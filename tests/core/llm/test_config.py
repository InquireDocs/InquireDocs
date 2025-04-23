from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_settings():
    """Mock settings for all tests in this package"""
    with patch('app.core.llm.ollama.settings') as mock_settings, \
         patch('app.core.llm.openai.settings') as openai_mock_settings:

        # Mock Ollama settings
        mock_settings.ollama_base_url = "http://localhost:11434"
        mock_settings.ollama_default_model = "llama2"
        mock_settings.ollama_default_embeddings_model = "llama2:embed"
        mock_settings.default_model_temperature = 0.7
        mock_settings.default_max_tokens = 1024

        # Mock OpenAI settings
        openai_mock_settings.openai_api_key = "test-api-key"
        openai_mock_settings.openai_default_model = "gpt-3.5-turbo"
        openai_mock_settings.openai_default_embeddings_model = "text-embedding-ada-002"
        openai_mock_settings.default_model_temperature = 0.7
        openai_mock_settings.default_max_tokens = 1024

        yield mock_settings
