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
