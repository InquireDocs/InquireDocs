from fastapi import APIRouter

from app.api.v1.endpoints.git import router as git_router
from app.api.v1.endpoints.summarizer import router as summarizer_router
from app.api.v1.endpoints.retriever import router as retriever_router


router = APIRouter()

router.include_router(git_router, prefix="/git", tags=["git"])
router.include_router(
    summarizer_router, prefix="/summarizer", tags=["summarizer"]
)
router.include_router(retriever_router, prefix="/retriever", tags=["retriever"])
