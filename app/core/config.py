import logging
import os

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel

from app.services import llm


logger = logging.getLogger(__name__)

# Load environment variables from a .env file if it exists
load_dotenv()


def parse_bool(value: str):
    """Helper function to parse a boolean environment variable."""
    logger.info("Parsing boolean variable. Value: %s", value)
    return value.lower() == "true"


def parse_int(value: str):
    """Helper function to parse an integer environment variable with a custom
    exception.
    """
    try:
        return int(value)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid integer value: {value}") from e


def parse_float(value: str):
    """Helper function to parse an float environment variable with a custom
    exception.
    """
    try:
        return float(value)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid float: {value}") from e


class _Settings:
    """Application configuration via environment variables.

    Picks up environment variables, check their type and map them
    to a field in this class that can be accessed all over the
    application.
    """

    def __init__(self):
        self.load()

    def load(self):
        self.debug: bool = parse_bool(os.getenv("DEBUG", "false"))
        self.project_name: str = os.getenv("PROJECT_NAME", "InquireDocs")
        enabled_llm_providers: str = os.getenv("ENABLED_LLM_PROVIDERS", "ollama")

        self.enabled_llm_providers = enabled_llm_providers.split(",")

        self.llm_models = {}

        if "ollama" in self.enabled_llm_providers:
            logger.info("Using Ollama for LLM and embeddings")
            server_url: str = os.getenv("OLLAMA_SERVER_URL", "http://localhost:11434")
            embeddings_model: str = os.getenv("OLLAMA_EMBEDDINGS_MODEL", "all-minilm")
            ai_model: str = os.getenv("OLLAMA_AI_MODEL", "llama3.2:1b")
            model_temperature: str = parse_float(os.getenv("OLLAMA_MODEL_TEMPERATURE", "0"))

            self.llm_models["ollama"] = {
                "embeddings": llm.get_ollama_embeddings_model(server_url, embeddings_model),
                "llm": llm.get_ollama_model(server_url, ai_model, model_temperature),
            }

        if "openai" in self.enabled_llm_providers:
            logger.info("Using OpenAI for LLM and embeddings")
            api_key: str = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY is required when LLM is 'openai'")
            embeddings_model: str = os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")
            ai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            model_temperature: str = parse_float(os.getenv("OPENAI_MODEL_TEMPERATURE", "0"))
            self.llm_models["openai"] = {
                "embeddings": llm.get_openai_embeddings_model(api_key, embeddings_model),
                "llm": llm.get_openai_model(api_key, ai_model, model_temperature),
            }

    def get_embeddings_model(self, provider: str) -> Embeddings:
        if provider in self.llm_models:
            return self.llm_models[provider]["embeddings"]
        else:
            raise ValueError(f"The provider {provider} is not in the list of enabled providers {self.enabled_llm_providers}")  # noqa: E501

    def get_ai_model(self, provider: str) -> BaseChatModel:
        if provider in self.llm_models:
            return self.llm_models[provider]["llm"]
        else:
            raise ValueError(f"The provider {provider} is not in the list of enabled providers {self.enabled_llm_providers}")  # noqa: E501


settings = _Settings()
