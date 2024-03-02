from fastapi import APIRouter, Response, status


router = APIRouter(prefix="/pdf", tags=["api", "v1", "pdf"])


@router.get("/")
def get_pdfs(response: Response):
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "NOT IMPLEMENTED"


@router.post("/")
def add_pdf(response: Response):
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "NOT IMPLEMENTED"


@router.put("/")
def update_pdf(response: Response):
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "NOT IMPLEMENTED"


@router.delete("/")
def delete_pdf(response: Response):
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "NOT IMPLEMENTED"
