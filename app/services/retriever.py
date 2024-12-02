import logging

from app.core.config import settings
from app.models.schema import QuestionRequest


logger = logging.getLogger(__name__)


def get_answer(request: QuestionRequest):
    """Gets an answer from the LLM for the question in the request.
    Args:
        request: A QuestionRequest with all the data required to
                 elaborate the answer.

    Returns:
        The answer to the question asked.
    """
    logger.debug("Answering question")

    if request.question == "":
        return "Please provide the question to get an answer"

    try:
        # # Use RAG
        # if request.use_rag:
        #     # Get retriever
        #     try:
        #         db_connection = DatabaseConnection(
        #             retriever_score_threshold=0.50
        #         )
        #         retriever = db_connection.get_retriever()
        #     except (ValueError, Exception) as e:
        #         logger.error("Error connecting to DB. %s", e)
        #         retriever = None
        #     return get_answer_with_rag(request.question, retriever)

        # Elaborate answer without RAG
        answer = settings.llm.invoke([("human", request.question)])
        response = {
            "answer": answer.content
        }
        return response
    except (ValueError, Exception) as e:
        msg = "Error generating answer"
        logger.error("%s: %s", msg, e)
        raise ValueError(msg) from e


# def get_answer_with_rag(question: str, retriever):
#     rag_prompt = (
#     "You are an assistant for question-answering tasks. "
#      "Use the following pieces of retrieved context to answer the question. "
#      "If you don't know the answer, say that you don't know. "
#      "Use no more than 15 sentences and keep the answer concise."
#      "\n\n"
#      "{context}"
#     )

#     prompt = ChatPromptTemplate.from_messages(
#         [
#             ("system", rag_prompt),
#             ("human", "{input}"),
#         ]
#     )

#     question_answer_chain = create_stuff_documents_chain(settings.llm, prompt)
#     rag_chain = create_retrieval_chain(retriever, question_answer_chain)
#     response = rag_chain.invoke({"input": question})
#     return response
