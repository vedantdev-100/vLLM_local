from fastapi.testclient import TestClient

from llm_service.api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_invalid_chat_request():

    response = client.post(
        "/api/v1/chat",
        json={
            "messages": []
        },
    )

    assert response.status_code == 422