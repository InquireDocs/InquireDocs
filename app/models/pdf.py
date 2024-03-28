from langchain_core.documents import Document
from langchain.indexes import SQLRecordManager, index
from langchain_community.document_loaders import PyPDFLoader

from app.core.logging_config import logger
import app.db.database as db


def add_pdf(file_path: str):
    """Load a PDF document and split it into chunks.
       Chunks are saved in the Vector Store.

    Args:
        file_path: Either a local or web path to a PDF file.

    Returns:
        TO DEFINE
    """
    logger.info("Add PDF from %s", file_path)

    # Create the loader from the PDF file.
    loader = PyPDFLoader(file_path)

    # Load the PDF file path and split it into chunks
    documents = loader.load_and_split()

    # Add source metadata to documents
    documents = [Document(page_content=doc.page_content, metadata={"source": file_path}) for doc in documents]

    # Add documentos into the database
    db.add_documents(documents)

    # logger.info("Documents")
    # logger.info(documents)

    # pg_store = PGVectorStore()
    # pg_store.add_documents(documents)
    return True


def update_pdf(file_path: str):
    """Update previously added PDF
    """
    logger.info("Update PDF - NOT IMPLEMENTED")
    return None


def delete_pdf(file_path: str):
    """Delete PDF file with the source indicated.

    Args:
        file_path: Either a local or web path to a PDF file.

    Returns:
        TO DEFINE
    """
    logger.info("Delete PDF %s", file_path)
    db.delete_documents_with_source(file_path)
    return True
