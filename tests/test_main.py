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

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "endpoints": {
            "api": "http://testserver/api",
            "docs": "http://testserver/docs",
            "health": "http://testserver/health",
        }
    }


def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("health")

    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
