import os

import pytest
from unittest.mock import patch

from app.core.config import parse_bool, parse_float, parse_int, settings


@pytest.fixture(scope="session", autouse=True)
def mock_load_dotenv():
    """Mock the load_dotenv function to do nothing during tests."""
    with patch("app.core.config.load_dotenv"):
        yield


@pytest.fixture(autouse=True)
def clear_env():
    """Clear specific environment variables before each test to ensure test isolation."""

    keys_to_clear = [
        "DEBUG", "PROJECT_NAME", "LLM_PROVIDER",
        "OLLAMA_SERVER_URL", "OLLAMA_EMBEDDINGS_MODEL", "OLLAMA_AI_MODEL",
        "OPENAI_API_KEY", "OPENAI_EMBEDDINGS_MODEL", "OPENAI_MODEL", "OPENAI_MODEL_TEMPERATURE"
    ]

    for key in keys_to_clear:
        os.environ.pop(key, None)


@pytest.mark.parametrize("name, value_to_test, expected_value", [
  ("true-value-true", "true", True),
  ("true-value-True", "True", True),
  ("true-value-TRUE", "TRue", True),
  ("true-value-TRUE", "TRUE", True),
  ("false-value-false", "false", False),
  ("false-value-False", "False", False),
  ("false-value-FALSE", "FALSE", False),
  ("false-value-anything", "anything", False),
])
def test_parse_bool(name: str, value_to_test: str, expected_value: bool) -> None:
    """Test `parse_bool` function"""
    actual_value = parse_bool(value_to_test)
    assert actual_value == expected_value, f"{name}: Expected {expected_value}, got {actual_value}"


@pytest.mark.parametrize("name, value_to_test, expected_value, expected_exception_message", [
  ("test-valid_value", "5", 5, None),
  ("test-negative-value", "-10", -10, None),
  ("test-zero-value", "0", 0, None),
  ("test-float-value", "5.8", None, "Invalid integer value: 5.8"),
  ("test-not-a-number", "TEXT", None, "Invalid integer value: TEXT"),
])
def test_parse_int(name: str, value_to_test: str, expected_value: int, expected_exception_message: str) -> None:
    """Test `parse_int` function"""
    try:
        actual_value = parse_int(value_to_test)
        assert actual_value == expected_value, f"{name}: Expected {expected_value}, got {actual_value}"
    except ValueError as actual_exception:
        assert str(actual_exception) == expected_exception_message


@pytest.mark.parametrize("name, value_to_test, expected_value, expected_exception_message", [
  ("test-valid_value", "4.8", 4.8, None),
  ("test-negative-value", "-10.5", -10.5, None),
  ("test-zero-value", "0", 0, None),
  ("test-positive-integer-value", "5", 5, None),
  ("test-negative-integer-value", "-3", -3, None),
  ("test-float-value-invalid", "5..0", None, "Invalid float value: 5..0"),
  ("test-not-a-number", "TEXT", None, "Invalid float value: TEXT"),
])
def test_parse_float(name: str, value_to_test: str, expected_value: int, expected_exception_message: str) -> None:
    """Test `parse_float` function"""
    try:
        actual_value = parse_float(value_to_test)
        assert actual_value == expected_value, f"{name}: Expected {expected_value}, got {actual_value}"
    except ValueError as actual_exception:
        assert str(actual_exception) == expected_exception_message


def test_debug_mode():
    with patch.dict(os.environ, {"DEBUG": "true"}):
        settings.load()
        assert settings.debug is True


def test_set_project_name():
    with patch.dict(os.environ, {"PROJECT_NAME": "Test Project"}):
        settings.load()
        assert settings.project_name == "Test Project"


@patch("app.services.llm.get_ollama_embeddings_model")
@patch("app.services.llm.get_ollama_model")
def test_default_settings(mock_get_ollama_model, mock_get_ollama_embeddings_model):
    settings.load()

    assert settings.debug is False
    assert settings.project_name == "InquireDocs"
    assert settings.llm_provider == "ollama"

    mock_get_ollama_embeddings_model.assert_called_once_with("http://localhost:11434", "all-minilm")
    mock_get_ollama_model.assert_called_once_with("http://localhost:11434", "llama3.2:1b")


@patch("app.services.llm.get_ollama_embeddings_model")
@patch("app.services.llm.get_ollama_model")
def test_ollama_custom_settings(mock_get_ollama_model, mock_get_ollama_embeddings_model):
    with patch.dict(os.environ, {
      "OLLAMA_SERVER_URL": "http://127.0.0.1:1234",
      "OLLAMA_EMBEDDINGS_MODEL": "test_embeddings_model",
      "OLLAMA_AI_MODEL": "test_ai_model",
    }):
        settings.load()

        assert settings.debug is False
        assert settings.project_name == "InquireDocs"
        assert settings.llm_provider == "ollama"

        mock_get_ollama_embeddings_model.assert_called_once_with("http://127.0.0.1:1234", "test_embeddings_model")
        mock_get_ollama_model.assert_called_once_with("http://127.0.0.1:1234", "test_ai_model")


@patch("app.services.llm.get_openai_embeddings_model")
@patch("app.services.llm.get_openai_model")
def test_openai_default_settings(mock_get_openai_model, mock_get_openai_embeddings_model):
    with patch.dict(os.environ, {
      "LLM_PROVIDER": "openai",
      "OPENAI_API_KEY": "test-api-key"
    }):
        settings.load()

        settings_instance = settings  # Ensure singleton-like behavior

        assert settings_instance.llm_provider == "openai"

        mock_get_openai_embeddings_model.assert_called_once_with("test-api-key", "text-embedding-3-small")
        mock_get_openai_model.assert_called_once_with("test-api-key", "gpt-4o-mini", 0)


def test_openai_settings_missing_api_key2():
    with pytest.raises(ValueError, match="OPENAI_API_KEY is required when LLM is set to 'openai'"):
        with patch.dict(os.environ, {"LLM_PROVIDER": "openai"}):
            settings.load()


@patch("app.services.llm.get_openai_embeddings_model")
@patch("app.services.llm.get_openai_model")
def test_openai_custom_settings(mock_get_openai_model, mock_get_openai_embeddings_model):
    with patch.dict(os.environ, {
      "LLM_PROVIDER": "openai",
      "OPENAI_API_KEY": "test-api-key",
      "OPENAI_EMBEDDINGS_MODEL": "test-embedding-model",
      "OPENAI_MODEL": "test-model",
      "OPENAI_MODEL_TEMPERATURE": "0.2"
    }):
        settings.load()

        settings_instance = settings  # Ensure singleton-like behavior

        assert settings_instance.llm_provider == "openai"

        mock_get_openai_embeddings_model.assert_called_once_with("test-api-key", "test-embedding-model")
        mock_get_openai_model.assert_called_once_with("test-api-key", "test-model", 0.2)
