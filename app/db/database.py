from langchain_core.vectorstores import VectorStore

# TODO:
# [ ] Use indexing API: https://python.langchain.com/docs/how_to/indexing/


class Database():

    def __init__(self, vector_store: VectorStore) -> None:
        self.vector_store = vector_store
