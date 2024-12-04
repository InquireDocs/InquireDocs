import pytest
from unittest.mock import MagicMock, patch
from langchain_core.documents import Document

from app.models.schema import SummaryRequest
from app.services.summarizer import get_summary_types, generate_summary


def test_get_summary_types_return_structure():
    """Test that get_summary_types returns a list"""
    result = get_summary_types()
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, dict)
        assert "name" in item
        assert "display_name" in item
        assert "description" in item
        assert len(item.keys()) == 3


@patch("app.services.summarizer.settings.get_ai_model")
@patch("app.services.summarizer.create_stuff_documents_chain")
def test_generate_summary_success(mock_create_stuff_documents_chain, mock_get_ai_model):
    """Test successful summary generation"""
    mock_summary_request = SummaryRequest(
        text="Sample text for summarization",
        summary_type="concise",
        llm_provider="test_ai",
    )

    # Mock the create_stuff_documents_chain and its invoke method
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("LLM Error")
    mock_get_ai_model.return_value = mock_llm

    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {"output_text": "Generated summary"}
    mock_create_stuff_documents_chain.return_value = mock_chain

    # Call the generate_summary function
    response = generate_summary(mock_summary_request)

    # Assertions
    assert response == {"output_text": "Generated summary"}

    # Verify chain creation
    mock_create_stuff_documents_chain.assert_called_once()

    # Verify chain invocation
    mock_chain.invoke.assert_called_once_with(
        {"context": [Document(page_content=mock_summary_request.text)]}
    )


def test_generate_summary_with_empty_text():
    """Test summary generation with empty text"""
    request = SummaryRequest(text="", summary_type="concise", llm_provider="test_ai")

    response = generate_summary(request)
    assert response == "Please provide the text you would like summarized"


def test_generate_summary_with_invalid_summary_type():
    """Test summary generation with an invalid summary type"""
    request = SummaryRequest(
        text="Sample text", summary_type="invalid_type", llm_provider="test_ai"
    )
    with pytest.raises(ValueError, match="Error generating summary"):
        generate_summary(request)


@patch("app.services.summarizer.settings.get_ai_model")
def test_generate_summary_llm_error(mock_get_ai_model):
    """Test error handling when LLM fails"""
    request = SummaryRequest(text="Sample text", summary_type="concise", llm_provider="test_ai")

    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("LLM Error")
    mock_get_ai_model.return_value = mock_llm

    with pytest.raises(ValueError, match="Error generating summary"):
        generate_summary(request)
