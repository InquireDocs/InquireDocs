import logging

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document

from app.core.config import settings
from app.models.schema import SummaryRequest


logger = logging.getLogger(__name__)


SUMMARY_TYPES = {
  "concise": {
    "display_name": "Concise summary",
    "description": "Write a concise summary of the text",
    "prompt": """Write a concise summary of the following:
{context}
CONCISE SUMMARY:
"""
  },
  "detailed": {
    "display_name": "Detailed summary",
    "description": "Provide a detailed summary of the text",
    "prompt": """Provide a detailed summary of the following text:
{context}
DETAILED SUMMARY:
"""
  },
  "question": {
    "display_name": "Generate questions",
    "description": "Generate questions based on the text",
    "prompt": """Generate questions based on the following text:
{context}
QUESTIONS:
"""
  },
}


def get_summary_types():
    """Return the supported summary types"""
    return [
        {
            "name": key,
            "display_name": value["display_name"],
            "description": value["description"]
        }
        for key, value in SUMMARY_TYPES.items()
    ]


def generate_summary(request: SummaryRequest) -> str:
    """Generate a summary from the text provided in the arguments
    Args:
        request: A SummaryRequest with all the data required to create the summary.

    Returns:
        The summary of the text provided.
    """
    logger.debug("Generating summary")

    request_text = request.text
    request_type = request.summary_type

    try:
        # Define LLM
        llm = settings.llm

        # Define prompt
        summary_type = SUMMARY_TYPES.get(request_type)
        prompt_template = summary_type.get("prompt")
        prompt = PromptTemplate.from_template(prompt_template)

        # Define StuffDocumentsChain
        stuff_chain = create_stuff_documents_chain(llm, prompt)

        # Run summarize on the text
        docs = [ Document(page_content=request_text) ]
        response = stuff_chain.invoke({"context": docs})

        return response
    except (ValueError, Exception) as e:
        msg = "Error generating summary"
        logger.error("%s: %s", msg, e)
        raise ValueError(msg) from e
