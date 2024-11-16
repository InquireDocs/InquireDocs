from pydantic import BaseModel


class SummaryRequest(BaseModel):
    """Model to define a summary request"""
    text: str
    summary_type: str
