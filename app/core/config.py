from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = Field(default=False)

    # Project settings
    project_name: str = Field(default="InquireDocs")

    # Generic AI
    default_summary_type: str = Field(default="concise")
    default_model_temperature: float = Field(default=0.0)
    default_max_tokens: int = Field(default=1000)

    # OpenAI
    openai_api_key: Optional[str] = Field(default=None)
    openai_default_embeddings_model: Optional[str] = Field(default="text-embedding-3-small")
    openai_default_model: Optional[str] = Field(default="gpt-4o-mini")

    # Ollama
    ollama_base_url: Optional[str] = Field(default="http://localhost:11434")
    ollama_default_embeddings_model: Optional[str] = Field(default="all-minilm")
    ollama_default_model: Optional[str] = Field(default="llama3:8b")

    # Available AI providers based on provided credentials
    @property
    def available_ai_providers(self):
        providers = ["ollama"]  # Ollama is always available as it can run locally
        if self.openai_api_key:
            providers.append("openai")
        return providers

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)


settings = Settings()
