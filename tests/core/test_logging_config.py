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
from importlib import reload
import logging
from unittest.mock import patch

from app.core.config import Settings
import app.core.logging_config as logger_configuration


def test_logger_configuration_debug_enabled(monkeypatch):
    """Test basic logger configuration with DEBUG flag set to true"""
    monkeypatch.setenv("DEBUG", "true")
    with patch("app.core.config.settings") as test_settings:
        test_settings.return_value = Settings(_env_file=None)
        reload(logger_configuration)
        assert logging.getLogger().level == logging.DEBUG
