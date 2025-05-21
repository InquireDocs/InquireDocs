from importlib import reload
import logging
from unittest.mock import patch

from app.core.config import Settings
import app.core.logging_config as logger_configuration


def test_logger_configuration_debug_enabled(monkeypatch):
    """Test basic logger configuration with DEBUG flag set to true"""
    monkeypatch.setenv('DEBUG', 'true')
    with patch('app.core.config.settings') as test_settings:
        test_settings.return_value = Settings(_env_file=None)
        reload(logger_configuration)
        assert logging.getLogger().level == logging.DEBUG
