from typing import List, Tuple

import chromadb

# from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.indexes import SQLRecordManager, index
from langchain.schema.document import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import Chroma

from app.core.config import settings


persist_directory = str(settings.DATA_PATH)

collection_name = "documents"

chroma_client = chromadb.PersistentClient(path=persist_directory)

chroma = Chroma(
  client=chroma_client,
  embedding_function=GPT4AllEmbeddings(),
  persist_directory=persist_directory,
  collection_name=collection_name
)

retriever = chroma.as_retriever()

sql_db_uri = "sqlite:///db/inquire_docs_index.db"
db = SQLDatabase.from_uri(sql_db_uri)
namespace = "chromadb/" + collection_name
record_manager = SQLRecordManager(
    namespace, db_url=sql_db_uri
)
record_manager.create_schema()

# class Database():

#         self.__text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=256)
#         self.__

#     def __save_embeddings(self, chunks):
#         """Persist embeddings into local ChromDB vector store
#         @param chunks: Chunks to persist
#         """
#         self.__chroma.add_documents(documents=chunks)
#         self.__chroma.persist()

#     # LangChain document loaders
#     # https://python.langchain.com/docs/integrations/document_loaders

#     def load_pdf_document(self, file_path: str):
#         """Load PDF document
#            https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf#using-pypdf

#         @param file_path: Path of the PDF file to load.
#         """
#         loader = PyPDFLoader(file_path)
#         documents = loader.load_and_split(text_splitter=self.__text_splitter)
#         self.__save_embeddings(documents)

#     def load_pdf_directory(self, path: str, recursive=False):
#         """Load PDF documents from path
#            https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf#pypdf-directory

#         @param path: Path containing the PDF to load.
#         @recursive: Boolean variable to indicate if subfolders are included or not. Defaults to False.
#         """
#         loader = PyPDFDirectoryLoader(path=path, recursive=recursive)
#         documents = loader.load()
#         chunks = self.__text_splitter.split_documents(documents)
#         self.__save_embeddings(chunks)

#     ##################
#     # Chroma retrieval

#     def similarity_search(self, question: str) -> List[Document]:
#         """ Search in database all documents that matches certain question.
#         @param question: Question to look in the documents
#         """

#         documents = self.__chroma.similarity_search(question)
#         return documents

#     def similarity_search_with_relevance_scores(self, question: str, return_docs: int=4, score_threshold: float=0) -> List[Tuple[Document, float]]:
#         """ Return docs and relevance scores in the range [0, 1]. 0 is dissimilar, 1 is most similar.
#         @param question: Question to look in the documents
#         @param return_docs: Number of Documents to return. Defaults to 4.
#         @param score_threshold: Optional, a floating point value between 0 to 1 to filter the resulting set of retrieved docs. Defaults to 0.
#         """
#         documents = self.__chroma.similarity_search_with_relevance_scores(query=question, k=return_docs, score_threshold=score_threshold)
#         return documents

#     def retrieve(self, question: str):
#         """ Retrieve documents from DB matching the question.
#         @param question: Question to look in the documents
#         """
#         documents = self.__retriever.invoke(question)
#         return documents

#     def update_document(self, document_id: str, document: Document) -> None:
#         """Update a document in the collection.
#         @param document_id: ID of the document to update.
#         @param document: Document to update.
#         """
#         self.__chroma.update_document(document_id, document)
