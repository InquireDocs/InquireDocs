import logging

import os
from dotenv import load_dotenv

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
        self.llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")

        match self.llm_provider:
            case "ollama":
                logger.info("Using Ollama for LLM and embeddings")
                ollama_server_url: str = os.getenv(
                    "OLLAMA_SERVER_URL", "http://localhost:11434"
                )
                ollama_embeddings_model: str = os.getenv(
                    "OLLAMA_EMBEDDINGS_MODEL", "all-minilm"
                )
                ollama_ai_model: str = os.getenv(
                    "OLLAMA_AI_MODEL", "llama3.2:1b"
                )
                ollama_model_temperature: str = parse_float(
                    os.getenv("OLLAMA_MODEL_TEMPERATURE", "0")
                )
                self.embeddings = llm.get_ollama_embeddings_model(
                    ollama_server_url, ollama_embeddings_model
                )
                self.llm = llm.get_ollama_model(
                    ollama_server_url, ollama_ai_model, ollama_model_temperature
                )
            case "openai":
                logger.info("Using OpenAI for LLM and embeddings")
                openai_api_key: str = os.getenv("OPENAI_API_KEY")
                if not openai_api_key:
                    raise ValueError(
                        "OPENAI_API_KEY is required when LLM is 'openai'"
                    )
                openai_embeddings_model: str = os.getenv(
                    "OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small"
                )
                openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
                openai_model_temperature: str = parse_float(
                    os.getenv("OPENAI_MODEL_TEMPERATURE", "0")
                )
                self.embeddings = llm.get_openai_embeddings_model(
                    openai_api_key, openai_embeddings_model
                )
                self.llm = llm.get_openai_model(
                    openai_api_key, openai_model, openai_model_temperature
                )


settings = _Settings()
