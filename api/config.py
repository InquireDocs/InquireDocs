from pathlib import Path
import sys

from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    """Application configuration via environment variables.

    Picks up environment variables, check their type and map them
    to a field in this class that can be accessed all over the
    application.

    A field like `app_path` will be looking for the environment
    variable `APP_PATH`.
    """

    # Prepare local paths
    app_path: Path = Path.home().joinpath('.inquiredocs')
    data_path: Path = app_path.joinpath('data')
    llm_path: Path = app_path.joinpath('llm')

    debug: bool = False

    # openai_api_key: str

    postgres_driver: str = "psycopg2"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "test"
    postgres_user: str = "example"
    postgres_password: str = "example"


settings = _Settings()
