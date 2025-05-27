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
import os
from unittest import mock

import pytest

from app.core.config import Settings


@pytest.fixture(autouse=True)
def clear_env_and_reload():
    """
    Ensure each test runs with a completely clean environment.
    Any environment variables are wiped out and then restored after.
    """
    with mock.patch.dict(os.environ, {}, clear=True):
        yield


def test_defaults():
    """
    If no environment variables are set, all defaults should apply.
    """
    test_settings = Settings(_env_file=None)
    assert test_settings.debug is False
    assert test_settings.project_name == "InquireDocs"
    assert test_settings.default_summary_type == "concise"
    assert test_settings.default_model_temperature == 0.0
    assert test_settings.default_max_tokens == 1000
    assert test_settings.openai_api_key is None
    assert test_settings.available_ai_providers == ["ollama"]


@pytest.mark.parametrize(
    "env_vars, field, expected",
    [
        ({"DEBUG": "true"}, "debug", True),
        ({"PROJECT_NAME": "TestProject"}, "project_name", "TestProject"),
        ({"DEFAULT_SUMMARY_TYPE": "detailed"}, "default_summary_type", "detailed"),
        ({"DEFAULT_MODEL_TEMPERATURE": "0.5"}, "default_model_temperature", 0.5),
        ({"DEFAULT_MAX_TOKENS": "200"}, "default_max_tokens", 200),
        ({"OPENAI_API_KEY": "test-api-key"}, "openai_api_key", "test-api-key"),
        (
            {"OPENAI_DEFAULT_EMBEDDINGS_MODEL": "test-embeddings"},
            "openai_default_embeddings_model",
            "test-embeddings",
        ),
        ({"OPENAI_DEFAULT_MODEL": "test-model"}, "openai_default_model", "test-model"),
        ({"OLLAMA_BASE_URL": "http://test-url:11434"}, "ollama_base_url", "http://test-url:11434"),
        (
            {"OLLAMA_DEFAULT_EMBEDDINGS_MODEL": "test-ollama-embeddings"},
            "ollama_default_embeddings_model",
            "test-ollama-embeddings",
        ),
        (
            {"OLLAMA_DEFAULT_MODEL": "test-ollama-model"},
            "ollama_default_model",
            "test-ollama-model",
        ),
    ],
)
def test_env_overrides(monkeypatch, env_vars, field, expected):
    """
    Override individual fields via environment variables.
    """
    for key, val in env_vars.items():
        monkeypatch.setenv(key, val)
    test_settings = Settings(_env_file=None)
    assert getattr(test_settings, field) == expected


def test_available_providers_without_openai():
    """
    Without an OpenAI key, only Ollama should be listed.
    """
    test_settings = Settings(_env_file=None)
    assert test_settings.available_ai_providers == ["ollama"]


def test_available_providers_with_openai(monkeypatch):
    """
    With OPENAI_API_KEY present, both Ollama and OpenAI appear.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    test_settings = Settings(_env_file=None)
    assert set(test_settings.available_ai_providers) == {"ollama", "openai"}


def test_case_insensitive_loading(monkeypatch):
    """
    Confirm that case_sensitive=False allows lowercase keys.
    """
    monkeypatch.setenv("project_name", "lowercaseName")
    test_settings = Settings(_env_file=None)
    assert test_settings.project_name == "lowercaseName"
