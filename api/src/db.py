import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import GPT4AllEmbeddings


PERSIST_DIRECTORY = ".db_local"


class Database():

    def __init__(self):
        self.client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
        self.langchain_chroma = Chroma(
            client=self.client,
            embedding_function=GPT4AllEmbeddings(),
            persist_directory=PERSIST_DIRECTORY
        )
