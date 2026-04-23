from fastapi import HTTPException, Request
from app.services.cache import redis_client
import logging

logger = logging.getLogger(__name__)

RATE_LIMIT = 5
WINDOW_SECONDS = 60


def get_client_identifier(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        first_hop = forwarded_for.split(",")[0].strip()
        if first_hop:
            return first_hop

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def check_rate_limit(request: Request):
    if not redis_client:
        return

    client_ip = get_client_identifier(request)
    redis_key = f"rate_limit:{client_ip}"

    try:
        current_count = redis_client.incr(redis_key)

        if current_count == 1:
            redis_client.expire(redis_key, WINDOW_SECONDS)

        if current_count > RATE_LIMIT:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later."
            )

    except HTTPException:
        raise

    except Exception as e:
        logger.warning("Rate limiter failed for %s: %s", redis_key, e)
        return