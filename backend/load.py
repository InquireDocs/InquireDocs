from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
import logging
import config


def load_documents():
    """Loading documents
    """
    logging.info("Loading documents")
    loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
    data = loader.load()
    return data


def create_chunks(data):
    """Create chunks from documents.
    @param data: Documents loaded
    """
    logging.info("Splitting documents into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)
    return chunks


def save_embeddings(chunks):
    """Persist embeddings into local ChromDB vector store
    @param chunks: Chinks to persist
    """
    logging.info("Persist embeddings into local ChromaDB")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=config.CHROMA_EMBEDDING_FUNCTION,
        persist_directory=config.CHROMA_PERSIST_DIRECTORY
    )
    vector_db.persist()
    logging.info("Ingestion completed")


if __name__ == "__main__":
    data = load_documents()
    chunks = create_chunks(data=data)
    save_embeddings(chunks=chunks)
