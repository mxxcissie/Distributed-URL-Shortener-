import pytest
from app.services.cache import redis_client


def clear_rate_limit_keys():
    if not redis_client:
        return
    for key in redis_client.keys("rate_limit:*"):
        redis_client.delete(key)


def test_rate_limit_on_shorten(client):
    if not redis_client:
        pytest.skip("Redis not configured")

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