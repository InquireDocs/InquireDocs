import logging

from langchain.document_loaders import PyPDFDirectoryLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Chroma

import config
from db import Database


# Langchain document loaders
# https://python.langchain.com/docs/integrations/document_loaders
def load_documents_chunks():
    """Loading documents and create chunks from them
    """
    logging.info("Loading documents")
    loader = PyPDFDirectoryLoader(path=config.PDF_DIRECTORY, recursive=True)
    documents = loader.load()

    logging.info("Splitting documents into chunks")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
    chunks = text_splitter.split_documents(documents)
    return chunks


def save_embeddings(chunks):
    """Persist embeddings into local ChromDB vector store
    @param chunks: Chinks to persist
    """
    logging.info("Load data into Chroma")
    vector_db = Database().langchain_chroma
    vector_db.add_documents(documents=chunks)

    logging.info("Persist embeddings into local ChromaDB")
    vector_db.persist()

    logging.info("Ingestion completed")


if __name__ == "__main__":
    chunks = load_documents_chunks()
    save_embeddings(chunks=chunks)
