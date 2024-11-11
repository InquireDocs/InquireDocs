from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    """Application configuration via environment variables.

    Picks up environment variables, check their type and map them
    to a field in this class that can be accessed all over the
    application.
    """
    model_config = SettingsConfigDict(env_file='.env')

    debug: bool = Field(alias='DEBUG', default=False)
    project_name: str = Field(alias='PROJECT_NAME', default='InquireDocs')
    openai_api_token: str = Field(alias='OPENAI_API_KEY')


settings = _Settings()
