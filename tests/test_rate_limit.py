import pytest
from fastapi import Request
from app.services.cache import redis_client
from app.services.rate_limiter import get_client_identifier


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


def test_get_client_identifier_prefers_forwarded_for():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/shorten",
        "headers": [(b"x-forwarded-for", b"203.0.113.10, 10.0.0.5")],
        "client": ("10.0.0.5", 12345),
    }

    request = Request(scope)

    assert get_client_identifier(request) == "203.0.113.10"


def test_get_client_identifier_falls_back_to_socket_ip():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/shorten",
        "headers": [],
        "client": ("127.0.0.1", 12345),
    }

    request = Request(scope)

    assert get_client_identifier(request) == "127.0.0.1"