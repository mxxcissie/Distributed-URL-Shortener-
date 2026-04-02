from fastapi.testclient import TestClient
from app.main import app
from app.cache import redis_client

client = TestClient(app)


def test_stats_for_created_url():
    for key in redis_client.keys("rate_limit:*"):
        redis_client.delete(key)

    create_response = client.post(
        "/shorten",
        json={"original_url": "https://www.google.com"}
    )
    assert create_response.status_code == 200

    short_code = create_response.json()["short_code"]

    stats_response = client.get(f"/stats/{short_code}")
    assert stats_response.status_code == 200

    data = stats_response.json()
    assert data["short_code"] == short_code
    assert data["original_url"] == "https://www.google.com/"
    assert "click_count" in data
    assert "created_at" in data