from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = Field(default=False)

    # Project settings
    project_name: str = Field(default="InquireDocs")

    # Generic AI
    default_model_temperature: float = Field(default=0.0)
    default_max_tokens: int = Field(default=100)

    # OpenAI
    openai_api_key: Optional[str] = Field(default=None)
    openai_default_embeddings_model: Optional[str] = Field(default="text-embedding-3-small")
    openai_default_model: Optional[str] = Field(default="gpt-4o-mini")

    # Ollama
    ollama_base_url: Optional[str] = Field(default="http://localhost:11434")
    ollama_default_embeddings_model: Optional[str] = Field(default="all-minilm")
    ollama_default_model: Optional[str] = Field(default="llama3.2:1b")

    # Available services based on provided credentials
    @property
    def available_llm_providers(self):
        providers = []
        if self.openai_api_key:
            providers.append("openai")
        providers.append("ollama")  # Ollama is always available as it can run locally
        return providers

    # Chroma
    # CHROMA_PERSIST_DIRECTORY: str = Field(
    #     "/data/chroma",
    #     description="Directory to persist Chroma DB"
    # )

    # # Available services based on provided credentials
    # @property
    # def available_llm_providers(self):
    #     providers = []
    #     if self.OPENAI_API_KEY:
    #         providers.append("openai")
    #     if self.ANTHROPIC_API_KEY:
    #         providers.append("anthropic")
    #     providers.append("ollama")  # Ollama is always available as it can run locally
    #     return providers

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
