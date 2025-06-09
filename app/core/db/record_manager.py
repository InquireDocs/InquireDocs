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
from collections.abc import Iterable
from typing import Callable, Literal, Union

from langchain.indexes import SQLRecordManager, index
from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document
from langchain_core.indexing.base import DocumentIndex
from langchain_core.vectorstores import VectorStore


class SQLiteRecordManager():
    """Record Manager"""

    def __init__(self, record_manager_namespace: str,
                 cleanup: Literal["incremental", "full", "scoped_full", None] = "scoped_full",
                 source_id_key: Union[str, Callable[[Document], str], None] = None) -> None:
        self.instance = SQLRecordManager(
            record_manager_namespace,
            db_url="sqlite:///record_manager_cache.sql"
        )
        self.instance.create_schema()
        self.cleanup = cleanup
        self.source_id_key = source_id_key

    def index(self,
              documents_list: Union[BaseLoader, Iterable[Document]],
              vector_store: Union[VectorStore, DocumentIndex]) -> None:
        """invoke index function"""
        index(documents_list,
              self.instance,
              vector_store,
              cleanup=self.cleanup,
              source_id_key=self.source_id_key)
