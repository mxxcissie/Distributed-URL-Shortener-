from fastapi.testclient import TestClient
from app.main import app
from app.cache import redis_client

client = TestClient(app)


def clear_rate_limit_keys():
    if not redis_client:
        return
    for key in redis_client.keys("rate_limit:*"):
        redis_client.delete(key)


def test_shorten_url():
    clear_rate_limit_keys()

    response = client.post(
        "/shorten",
        json={"original_url": "https://www.google.com"}
    )

    assert response.status_code == 200

    data = response.json()
    assert "short_code" in data
    assert "short_url" in data
    assert data["short_url"].startswith("http://127.0.0.1:8000/")