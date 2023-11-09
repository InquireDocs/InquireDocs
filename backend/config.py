from langchain.embeddings import GPT4AllEmbeddings


CHROMA_PERSIST_DIRECTORY = ".db_local"
CHROMA_EMBEDDING_FUNCTION = GPT4AllEmbeddings()
