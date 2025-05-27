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

from app.core.llm import get_llm_provider

# from app.core.llm.openai import OpenAILLM
from app.core.llm.ollama import OllamaLLM


# TODO: Test NOT working. Needs fixing
# def test_get_openai_llm(monkeypatch):
#     """Test getting OpenAI LLM provider"""
#     monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
#     with patch('app.core.config.settings') as test_settings:
#         test_settings.return_value = Settings(_env_file=None)
#         llm = get_llm_provider("openai")
#         assert isinstance(llm, OpenAILLM)
#         assert llm.provider_name == "openai"


def test_get_ollama_llm():
    """Test getting Ollama LLM provider"""
    llm = get_llm_provider("ollama")
    assert isinstance(llm, OllamaLLM)
    assert llm.provider_name == "ollama"


def test_get_unknown_llm():
    """Test getting an unknown LLM provider raises exception"""
    with pytest.raises(ValueError, match="Provider unknown not available or not configured"):
        get_llm_provider("unknown")
