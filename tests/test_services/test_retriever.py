# import pytest
# from unittest.mock import MagicMock, patch
# from langchain_core.messages import BaseMessage

# from app.models.schema import QuestionRequest
# from app.services.retriever import get_answer


# @patch("app.services.retriever.settings.get_ai_model")
# def test_generate_summary_success(mock_get_ai_model):
#     """Test successful summary generation"""
#     mock_request = QuestionRequest(
#         question="What is the name of our planet?",
#         use_rag=False,
#         rag_retrieve_threshold=0.5,
#         llm_provider="test_ai",
#     )

#     # Mock the LLM return value
#     mock_llm = MagicMock()
#     mock_llm.invoke.return_value = BaseMessage(content="Earth", type="str")
#     mock_get_ai_model.return_value = mock_llm

#     # Call the generate_summary function
#     response = get_answer(mock_request)

#     # Assertions
#     assert response == {"answer": "Earth"}

#     # Verify LLM invocation
#     mock_llm.invoke.assert_called_once_with([("human", mock_request.question)])


# def test_get_answer_with_empty_question():
#     """Test generating an answer with empty question"""
#     request = QuestionRequest(
#         question="",
#         use_rag=False,
#         rag_retrieve_threshold=0.5,
#         llm_provider="test_ai",
#     )

#     response = get_answer(request)
#     assert response == "Please provide the question to get an answer"


# @patch("app.services.retriever.settings.get_ai_model")
# def test_get_answer_llm_error(mock_get_ai_model):
#     """Test error handling when LLM fails"""
#     request = QuestionRequest(
#         question="What is the name of our planet?",
#         use_rag=False,
#         rag_retrieve_threshold=0.5,
#         llm_provider="openai",
#     )

#     mock_llm = MagicMock()
#     mock_llm.invoke.side_effect = Exception("LLM Error")
#     mock_get_ai_model.return_value = mock_llm

#     # mock_get_ai_model.invoke.side_effect = Exception("LLM Error")
#     with pytest.raises(ValueError, match="Error generating answer"):
#         get_answer(request)
