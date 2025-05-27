# import os
# import pytest
# from unittest import mock

# from app.core.config import Settings, settings

# # 1) Disable loading of any .env file in Pydantic Settings
# import app.core.config
# app.core.config.Settings.ConfigDict.env_file = None

# from app.core.config import Settings

# @pytest.fixture(autouse=True)
# def clear_env_vars():
#     """
#     Autouse fixture to clear any environment variables that might affect Settings.
#     """
#     for var in list(os.environ):
#         if var.startswith(("OPENAI_", "OLLAMA_")) or var in {"DEBUG", "PROJECT_NAME"}:
#             del os.environ[var]
#     yield





# import os
# import pytest

# from app.core.config import Settings


# class TestSettings:
#     """Test suite for the Settings class and its instance."""

#     def test_default_values(self):
#         """Test that default values are set correctly."""
#         test_settings = Settings(_env_file=None)
#         assert test_settings.DEBUG is False
#         assert test_settings.PROJECT_NAME == "InquireDocs"
#         assert test_settings.default_summary_type == "concise"
#         assert test_settings.default_model_temperature == 0.0
#         assert test_settings.default_max_tokens == 1000
#         assert test_settings.openai_api_key is None
#         assert test_settings.openai_default_embeddings_model == "text-embedding-3-small"
#         assert test_settings.openai_default_model == "gpt-4o-mini"
#         assert test_settings.ollama_base_url == "http://localhost:11434"
#         assert test_settings.ollama_default_embeddings_model == "all-minilm"
#         assert test_settings.ollama_default_model == "llama3:8b"

#     def test_env_variable_override(self, monkeypatch):
#         """Test that environment variables properly override defaults."""

#         monkeypatch.setenv('DEBUG', 'true')
#         monkeypatch.setenv('PROJECT_NAME', 'TestProject')
#         monkeypatch.setenv('DEFAULT_SUMMARY_TYPE', 'detailed')
#         monkeypatch.setenv('DEFAULT_MODEL_TEMPERATURE', '0.5')
#         monkeypatch.setenv('DEFAULT_MAX_TOKENS', '200')
#         monkeypatch.setenv('OPENAI_API_KEY', 'test-api-key')
#         monkeypatch.setenv('OPENAI_DEFAULT_EMBEDDINGS_MODEL', 'test-embeddings')
#         monkeypatch.setenv('OPENAI_DEFAULT_MODEL', 'test-model')
#         monkeypatch.setenv('OLLAMA_BASE_URL', 'http://test-url:11434')
#         monkeypatch.setenv('OLLAMA_DEFAULT_EMBEDDINGS_MODEL', 'test-ollama-embeddings')
#         monkeypatch.setenv('OLLAMA_DEFAULT_MODEL', 'test-ollama-model')

#         test_settings = Settings(_env_file=None)
#         assert test_settings.DEBUG is True
#         assert test_settings.PROJECT_NAME == "TestProject"
#         assert test_settings.default_summary_type == "detailed"
#         assert test_settings.default_model_temperature == 0.5
#         assert test_settings.default_max_tokens == 200
#         assert test_settings.openai_api_key == "test-api-key"
#         assert test_settings.openai_default_embeddings_model == "test-embeddings"
#         assert test_settings.openai_default_model == "test-model"
#         assert test_settings.ollama_base_url == "http://test-url:11434"
#         assert test_settings.ollama_default_embeddings_model == "test-ollama-embeddings"
#         assert test_settings.ollama_default_model == "test-ollama-model"

#     def test_available_ai_providers_with_openai(self, monkeypatch):
#         """Test available_ai_providers property when OpenAI API key is provided."""
#         monkeypatch.setenv('OPENAI_API_KEY', 'test-api-key')
#         test_settings = Settings(_env_file=None)
#         providers = test_settings.available_ai_providers
#         assert len(providers) == 2
#         assert "openai" in providers
#         assert "ollama" in providers

#     def test_available_ai_providers_without_openai(self, monkeypatch):
#         """Test available_ai_providers property when OpenAI API key is not provided."""
#         monkeypatch.setenv('OPENAI_API_KEY', 'test-api-key')
#         test_settings = Settings(_env_file=None)
#         providers = test_settings.available_ai_providers
#         assert len(providers) == 1
#         assert "openai" not in providers
#         assert "ollama" in providers


#     # def test_settings_singleton(self):
#     #     """Test that the settings instance exists and is properly configured."""
#     #     assert settings is not None
#     #     assert isinstance(settings, Settings)
#     #     assert settings.PROJECT_NAME == "InquireDocs"  # Test one default value

#     # def test_case_sensitivity(self, monkeypatch):
#     #     """Test that configuration is case sensitive as specified."""
#     #     assert Settings.ConfigDict.case_sensitive is True

#     #     # This should not override the uppercase env var
#     #     with mock.patch.dict(os.environ, {"PROJECT_NAME": "LowercaseProject"}):
#     #         test_settings = Settings()
#     #         assert test_settings.PROJECT_NAME == "InquireDocs"  # Default value remains

#     #     # This should override (correct case)
#     #     with mock.patch.dict(os.environ, {"PROJECT_NAME": "UppercaseProject"}):
#     #         test_settings = Settings()
#     #         assert test_settings.PROJECT_NAME == "UppercaseProject"


# tests/conftest.py
