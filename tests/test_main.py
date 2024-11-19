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
