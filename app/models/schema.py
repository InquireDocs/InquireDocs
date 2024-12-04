from pydantic import BaseModel


class SummaryRequest(BaseModel):
    """Model to define a summary request"""

    summary_type: str
    text: str
    llm_provider: str


class QuestionRequest(BaseModel):
    """Model to define the question request"""

    question: str
    use_rag: bool
    rag_retrieve_threshold: float
    llm_provider: str
