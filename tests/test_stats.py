from app.cache import redis_client


def clear_rate_limit_keys():
    if not redis_client:
        return
    for key in redis_client.keys("rate_limit:*"):
        redis_client.delete(key)


def test_stats_for_created_url(client):
    clear_rate_limit_keys()

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