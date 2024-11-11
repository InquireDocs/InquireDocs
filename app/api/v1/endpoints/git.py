from fastapi import APIRouter, Response, status


router = APIRouter()


@router.get("/")
def hello_world(response: Response):
    """Process requests to add PDF files to vector store"""
    # pdf.add_pdf("asd")
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "NOT_IMPLEMENTED"
