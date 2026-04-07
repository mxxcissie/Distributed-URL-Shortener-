from fastapi import HTTPException, Request
from app.cache import redis_client

RATE_LIMIT = 5
WINDOW_SECONDS = 60


def check_rate_limit(request: Request):
    if not redis_client:
        return

    client_ip = request.client.host if request.client else "unknown"
    redis_key = f"rate_limit:{client_ip}"

    current_count = redis_client.get(redis_key)

    if current_count is None:
        redis_client.set(redis_key, 1, ex=WINDOW_SECONDS)
        return

    current_count = int(current_count)

    if current_count >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    redis_client.incr(redis_key)