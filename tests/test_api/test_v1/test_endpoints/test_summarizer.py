from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.models.schema import SummaryRequest


client = TestClient(app)
base_url_path = "api/v1/summarizer"
summary_types_endpoint = f"{base_url_path}/summary_types"
summarize_endpoint = f"{base_url_path}/summarize"


@patch("app.api.v1.endpoints.summarizer.get_summary_types")
def test_summary_types_empty_list(mock_get_types):
    """Test when no summary types are available"""
    mock_get_types.return_value = []
    response = client.get(summary_types_endpoint)

    assert response.status_code == 200
    assert response.json() == []
    mock_get_types.assert_called_once()


@patch("app.api.v1.endpoints.summarizer.get_summary_types")
def test_summary_types_successful(mock_get_types):
    """Test successful retrieval of summary types"""
    expected_types = [
        {
            "name": "type1",
            "display_name": "Type 1",
            "description": "This is the first summary type",
        },
        {
            "name": "type2",
            "display_name": "Type 2",
            "description": "This is the second summary type",
        },
    ]

    mock_get_types.return_value = expected_types
    response = client.get(summary_types_endpoint)

    assert response.status_code == 200
    assert response.json() == expected_types
    mock_get_types.assert_called_once()


@patch("app.api.v1.endpoints.summarizer.get_summary_types")
def test_summary_types_value_error(mock_get_types):
    """Test handling of ValueError from the service"""
    mock_get_types.side_effect = ValueError("Invalid configuration")
    response = client.get(summary_types_endpoint)

    assert response.status_code == 500
    assert response.json() == {"detail": "Error getting summary types."}
    mock_get_types.assert_called_once()


@patch("app.api.v1.endpoints.summarizer.get_summary_types")
def test_summary_types_general_exception(mock_get_types):
    """Test handling of general exceptions"""
    mock_get_types.side_effect = Exception("Unexpected error")
    response = client.get(summary_types_endpoint)

    assert response.status_code == 500
    assert response.json() == {"detail": "Error getting summary types."}
    mock_get_types.assert_called_once()


@patch("app.api.v1.endpoints.summarizer.generate_summary")
def test_summarize_successful(mock_generate):
    """Test successful text summarization"""
    test_request = SummaryRequest(
        summary_type="concise",
        text="This is a long text that needs to be summarized.",
    )
    expected_summary = "This is a summary."

    mock_generate.return_value = expected_summary

    response = client.post(summarize_endpoint, json=test_request.model_dump())

    assert response.status_code == 200
    assert response.json() == expected_summary
    mock_generate.assert_called_once_with(test_request)


@patch("app.api.v1.endpoints.summarizer.generate_summary")
def test_summarize_empty_text(mock_generate):
    """Test summarization with empty text"""
    test_request = SummaryRequest(text="", summary_type="concise")

    mock_generate.side_effect = ValueError("Text cannot be empty")

    response = client.post(summarize_endpoint, json=test_request.model_dump())

    assert response.status_code == 500
    assert response.json() == {"detail": "Error generating the summary."}
    mock_generate.assert_called_once_with(test_request)


@patch("app.api.v1.endpoints.summarizer.generate_summary")
def test_summarize_invalid_type(mock_generate):
    """Test summarization with invalid summary type"""
    test_request = SummaryRequest(
        text="Some text to summarize", summary_type="invalid_type"
    )

    mock_generate.side_effect = ValueError("Invalid summary type")

    response = client.post(summarize_endpoint, json=test_request.model_dump())

    assert response.status_code == 500
    assert response.json() == {"detail": "Error generating the summary."}
    mock_generate.assert_called_once_with(test_request)


@patch("app.api.v1.endpoints.summarizer.generate_summary")
def test_summarize_service_error(mock_generate):
    """Test handling of service errors"""
    test_request = SummaryRequest(
        text="Some text to summarize", summary_type="concise"
    )

    mock_generate.side_effect = Exception("Service error")

    response = client.post(summarize_endpoint, json=test_request.model_dump())

    assert response.status_code == 500
    assert response.json() == {"detail": "Error generating the summary."}
    mock_generate.assert_called_once_with(test_request)


def test_summarize_invalid_request_format():
    """Test handling of invalid request format"""
    invalid_request = {"invalid_field": "some text", "type": "short"}

    response = client.post(summarize_endpoint, json=invalid_request)

    assert response.status_code == 422  # FastAPI validation error
