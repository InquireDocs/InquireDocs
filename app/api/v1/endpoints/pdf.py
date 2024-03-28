from typing import List

from fastapi import APIRouter, Response, status
from langchain_core.documents import Document

import app.models.pdf as pdf


router = APIRouter()


@router.post("/", response_model=List[Document])
def add_pdf(response: Response):
    """Process requests to add PDF files to vector store"""
    pdf.add_pdf("asd")
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "Add PDF"


@router.put("/{item_id}", response_model=List[Document])
def update_pdf(response: Response):
    """Process requests to update PDF files on vector store"""
    pdf.update_pdf()
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "Update PDF"


@router.delete("/{item_id}", response_model=List[Document])
def delete_pdf(response: Response):
    """Process requests to delete PDF files from vector store"""
    pdf.delete_pdf()
    response.status_code = status.HTTP_501_NOT_IMPLEMENTED
    return "Delete PDF"
