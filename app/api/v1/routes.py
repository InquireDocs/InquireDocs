from fastapi import APIRouter

from app.api.v1.endpoints.git import router as git_router


router = APIRouter()

router.include_router(git_router, prefix="/git", tags=["git"])
