# from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
# from app.models.schema import QuestionRequest


client = TestClient(app)
base_url_path = "api/v1/retriever"
ask_endpoint = f"{base_url_path}/ask"
