from app.services.cache import redis_client


def clear_rate_limit_keys():
    if not redis_client:
        return
    for key in redis_client.keys("rate_limit:*"):
        redis_client.delete(key)


def test_redirect_to_original_url(client):
    clear_rate_limit_keys()

    create_response = client.post(
        "/shorten",
        json={"original_url": "https://www.google.com"}
    )
    assert create_response.status_code == 200

    short_code = create_response.json()["short_code"]

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)

    assert redirect_response.status_code in (307, 302)
    assert redirect_response.headers["location"] == "https://www.google.com/"

    stats_response = client.get(f"/stats/{short_code}")
    assert stats_response.status_code == 200
    assert stats_response.json()["click_count"] == 1