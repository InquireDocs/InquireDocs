import pytest
from unittest.mock import patch
from langchain_core.messages import BaseMessage


from app.models.schema import QuestionRequest
from app.services.retriever import get_answer


@patch("app.services.retriever.settings.llm")
def test_generate_summary_success(mock_llm):
    """Test successful summary generation"""
    mock_request = QuestionRequest(
        question="What is the name of our planet?",
        use_rag=False,
        rag_retrieve_threshold=0.5,
    )

    # Mock the LLM return value
    mock_llm.invoke.return_value = BaseMessage(content="Earth", type="str")

    # Call the generate_summary function
    response = get_answer(mock_request)

    # Assertions
    assert response == {"answer": "Earth"}

    # Verify LLM invocation
    mock_llm.invoke.assert_called_once_with([("human", mock_request.question)])


def test_get_answer_with_empty_question():
    """Test generating an answer with empty question"""
    request = QuestionRequest(
        question="", use_rag=False, rag_retrieve_threshold=0.5
    )

    response = get_answer(request)
    assert response == "Please provide the question to get an answer"


@patch("app.services.retriever.settings.llm")
def test_get_answer_llm_error(mock_llm):
    """Test error handling when LLM fails"""
    request = QuestionRequest(
        question="What is the name of our planet?",
        use_rag=False,
        rag_retrieve_threshold=0.5,
    )
    mock_llm.invoke.side_effect = Exception("LLM Error")
    with pytest.raises(ValueError, match="Error generating answer"):
        get_answer(request)
