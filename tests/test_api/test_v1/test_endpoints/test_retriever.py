from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.models.schema import QuestionRequest


client = TestClient(app)
base_url_path = "api/v1/retriever"
ask_endpoint = f"{base_url_path}/ask"


@patch("app.api.v1.endpoints.retriever.get_answer")
def test_successful_retrieval(mock_get_answer):
    """Test successful retrieval"""
    test_request = QuestionRequest(
        question="Which is the name of our planet?",
        use_rag=False,
        rag_retrieve_threshold=0.5,
    )
    expected_answer = "Earth"

    mock_get_answer.return_value = expected_answer

    response = client.post(ask_endpoint, json=test_request.model_dump())

    assert response.status_code == 200
    assert response.json() == expected_answer
    mock_get_answer.assert_called_once_with(test_request)


@patch("app.api.v1.endpoints.retriever.get_answer")
def test_retrieval_empty_question(mock_get_answer):
    """Test retrieval with empty question"""
    test_request = QuestionRequest(
        question="", use_rag=False, rag_retrieve_threshold=0.5
    )

    mock_get_answer.side_effect = ValueError("Text cannot be empty")

    response = client.post(ask_endpoint, json=test_request.model_dump())

    assert response.status_code == 500
    assert response.json() == {"detail": "Error answering the question."}
    mock_get_answer.assert_called_once_with(test_request)


@patch("app.api.v1.endpoints.retriever.get_answer")
def test_retrieval_service_error(mock_get_answer):
    """Test handling of service errors"""
    test_request = QuestionRequest(
        question="Which is the name of our planet?",
        use_rag=False,
        rag_retrieve_threshold=0.5,
    )

    mock_get_answer.side_effect = Exception("Service error")

    response = client.post(ask_endpoint, json=test_request.model_dump())

    assert response.status_code == 500
    assert response.json() == {"detail": "Error answering the question."}
    mock_get_answer.assert_called_once_with(test_request)


def test_retrieval_invalid_request_format():
    """Test handling of invalid request format"""
    invalid_request = {"invalid_field": "some question", "use_rag": False}

    response = client.post(ask_endpoint, json=invalid_request)

    assert response.status_code == 422  # FastAPI validation error
