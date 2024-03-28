from fastapi import APIRouter

from app.api.v1.endpoints import retrieval

router = APIRouter()

router.include_router(retrieval.router, prefix="/retrieval", tags=["retrieval"])
