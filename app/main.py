import logging

from fastapi import FastAPI, status, Request

from app.api.v1.routes import router as v1_router
from app.core.config import settings
from app.core.logging_config import root_logger  # This import ensures logging is configured


logger = logging.getLogger(__name__)

app = FastAPI(title=settings.project_name)

logger.info("Starting")

@app.get("/", status_code=status.HTTP_200_OK, tags=["root"])
def root(request: Request):
    """Root endpoint"""
    return {
      "endpoints": {
        "api": f"{request.url}api",
        "docs": f"{request.url}docs",
        "health": f"{request.url}health"
      }
    }

@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "OK"}

app.include_router(v1_router, prefix="/api/v1")
