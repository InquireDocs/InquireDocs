#  Copyright 2024-present Julian Nonino
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging

from fastapi import FastAPI, status, Request

# This import ensures logging is configured
from app.core.logging_config import root_logger  # noqa: F401

from app.api.v1.routes import router as v1_router
from app.core.config import settings


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
            "health": f"{request.url}health",
        }
    }


@app.get("/health", status_code=status.HTTP_200_OK, tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "OK"}


app.include_router(v1_router, prefix="/api/v1")
