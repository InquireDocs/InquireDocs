from langchain_chroma import Chroma

from app.core.config import settings
from app.db.database import Database


# https://python.langchain.com/api_reference/chroma/vectorstores/langchain_chroma.vectorstores.Chroma.html#langchain_chroma.vectorstores.Chroma

class ChromaDB(Database):

    def __init__(self) -> None:

        vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=settings.get_vector_store_embeddings_model(),
            # Where to save data locally, remove if not necessary
            persist_directory="./chroma_langchain_db",
        )
        super().__init__(vector_store)
