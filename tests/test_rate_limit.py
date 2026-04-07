import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.cache import redis_client

pytestmark = pytest.mark.skipif(
    redis_client is None,
    reason="Redis not configured"
)

client = TestClient(app)


def clear_rate_limit_keys():
    for key in redis_client.keys("rate_limit:*"):
        redis_client.delete(key)


def test_rate_limit_on_shorten():
    clear_rate_limit_keys()

    for _ in range(5):
        response = client.post(
            "/shorten",
            json={"original_url": "https://www.google.com"}
        )
        assert response.status_code == 200

    response = client.post(
        "/shorten",
        json={"original_url": "https://www.google.com"}
    )

    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded. Try again later."