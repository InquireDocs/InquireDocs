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
from fastapi import APIRouter

# from app.api.v1.endpoints.git import router as git_router
from app.api.v1.endpoints.llm import router as llm_router
from app.api.v1.endpoints.summarizer import router as summarizer_router


router = APIRouter()

# router.include_router(git_router, prefix="/git", tags=["git"])
router.include_router(llm_router, prefix="/llm", tags=["retriever"])
router.include_router(summarizer_router, prefix="/summarizer", tags=["summarizer"])
