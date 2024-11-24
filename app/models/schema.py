from pydantic import BaseModel


class SummaryRequest(BaseModel):
    """Model to define a summary request"""

    summary_type: str
    text: str
