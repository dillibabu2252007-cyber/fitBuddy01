from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "FitBuddy" in response.text


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_goal():
    response = client.post(
        "/generate-workout",
        data={
            "username": "Test User",
            "user_id": "TEST001",
            "age": 20,
            "weight": 65,
            "goal": "invalid",
            "intensity": "medium",
        },
    )
    assert response.status_code == 400
    assert "Invalid fitness goal" in response.text
