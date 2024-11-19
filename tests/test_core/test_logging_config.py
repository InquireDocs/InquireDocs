import logging
import os

import pytest
from unittest.mock import patch

from app.core.config import settings
import app.core.logging_config as logger_configuration
from importlib import reload


@pytest.fixture(scope="session", autouse=True)
def mock_load_dotenv():
    """Mock the load_dotenv function to do nothing during tests."""
    with patch("app.core.config.load_dotenv"):
        yield


@pytest.fixture(autouse=True)
def clear_env():
    """Clear DEBUG environment variable before each test to ensure test isolation."""
    os.environ.pop("DEBUG", None)


def test_logger_configuration_debug_enabled():
    """Test basic logger configuration with DEBUG flag set to true"""
    with patch.dict(os.environ, {"DEBUG": "true"}):
        settings.load()
        reload(logger_configuration)
        root_logger = logging.getLogger()
        expected_level = logging.DEBUG

        assert settings.debug is True
        assert root_logger.level == expected_level


def test_logger_configuration_debug_disabled():
    """Test basic logger configuration with DEBUG flag set to false"""
    with patch.dict(os.environ, {"DEBUG": "false"}):
        settings.load()
        reload(logger_configuration)
        root_logger = logging.getLogger()
        expected_level = logging.INFO

        assert settings.debug is False
        assert root_logger.level == expected_level
