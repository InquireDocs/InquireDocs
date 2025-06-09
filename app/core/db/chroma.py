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
import logging

import chromadb
from langchain_chroma import Chroma

from app.core.config import settings
from app.core.db.base import BaseDatabase
from app.core.db.record_manager import SQLiteRecordManager
from app.core.llm import get_llm_provider


logger = logging.getLogger(__name__)


class ChromaDb(BaseDatabase):
    """ChromaDB implementation"""

    def __init__(self, index_cleanup: str, index_source_id_key: str) -> None:
        """Initialize ChromaDb"""
        if "chroma" in settings.available_vector_store_providers:
            self.client = chromadb.HttpClient(
                host=settings.chroma_server_host,
                port=settings.chroma_server_port,
                ssl=settings.chroma_server_ssl,
                headers={"X-CHROMA-TOKEN": settings.chroma_server_token},
                tenant=settings.chroma_server_tenant,
                database=settings.chroma_server_database)

            self.collection_name = settings.chroma_server_collection_name

            embeddings_provider = get_llm_provider(settings.chroma_server_embeddings_provider)
            self.embedding_function = embeddings_provider.get_embeddings_provider()

            self.rm_namespace = f"{self.provider_name}/{self.collection_name}"
            self.record_manager = SQLiteRecordManager(self.rm_namespace,
                                                      index_cleanup,
                                                      index_source_id_key).instance

            self.vector_store = Chroma(
                client=self.client,
                collection_name=self.collection_name,
                embedding_function=self.embedding_function
            )
        else:
            logger.error("Chroma is not available provider. Check the settings and try again.")

    @property
    def provider_name(self) -> str:
        return "chroma"


# self.record_manager.index(documents_list, self.vector_store)
