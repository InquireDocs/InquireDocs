from pathlib import Path

from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """Application configuration via environment variables.

    Picks up environment variables, check their type and map them
    to a field in this class that can be accessed all over the
    application.
    """

    # Prepare local paths
    APP_PATH: Path = Path.home().joinpath('.inquiredocs')
    DATA_PATH: Path = APP_PATH.joinpath('data')
    LLM_PATH: Path = APP_PATH.joinpath('llm')

    # Get environment variables
    PROJECT_NAME: str = "InquireDocs"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = _Settings()
