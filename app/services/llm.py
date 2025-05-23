import logging

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_ollama import ChatOllama, OllamaEmbeddings


logger = logging.getLogger(__name__)


def get_ollama_embeddings_model(server_url: str, embeddings_model: str) -> OllamaEmbeddings:
    return OllamaEmbeddings(base_url=server_url, model=embeddings_model)


def get_ollama_model(server_url, ai_model, model_temperature) -> ChatOllama:
    return ChatOllama(base_url=server_url, model=ai_model, temperature=model_temperature)


def get_openai_embeddings_model(api_key, embeddings_model) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(openai_api_key=api_key, model=embeddings_model)


def get_openai_model(api_key, model, model_temperature) -> ChatOpenAI:
    return ChatOpenAI(api_key=api_key, temperature=model_temperature, model_name=model)
