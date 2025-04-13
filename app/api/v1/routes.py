from fastapi import APIRouter

# from app.api.v1.endpoints.git import router as git_router
from app.api.v1.endpoints.llm import router as llm_router
from app.api.v1.endpoints.summarizer import router as summarizer_router


router = APIRouter()

# router.include_router(git_router, prefix="/git", tags=["git"])
router.include_router(llm_router, prefix="/llm", tags=["retriever"])
router.include_router(summarizer_router, prefix="/summarizer", tags=["summarizer"])
