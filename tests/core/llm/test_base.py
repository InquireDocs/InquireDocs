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
from abc import ABC

# from typing import Optional

from app.core.llm.base import BaseLLM

# from langchain_core.embeddings import Embeddings


def test_base_llm_is_abstract():
    """Test that BaseLLM is an abstract base class"""
    assert issubclass(BaseLLM, ABC)

    # Verify we can't instantiate the base class
    with pytest.raises(TypeError):
        BaseLLM()


def test_provider_name_is_abstract():
    """Test that provider_name is an abstract property"""
    # We need to access the actual property, not the getter
    property_obj = BaseLLM.__dict__["provider_name"]
    assert property_obj.fget.__isabstractmethod__


def test_get_embeddings_provider_is_abstract():
    """Test that get_embeddings_provider is an abstract method"""
    assert BaseLLM.get_embeddings_provider.__isabstractmethod__


def test_ask_is_abstract():
    """Test that ask is an abstract method"""
    assert BaseLLM.ask.__isabstractmethod__
