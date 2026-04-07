import redis
from app.config import REDIS_URL

#redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        redis_client.ping()
    except Exception:
        redis_client = None


def get_cached_url(short_code: str):
    if not redis_client:
        return None
    return redis_client.get(short_code)


def set_cached_url(short_code: str, original_url: str):
    if not redis_client:
        return
    redis_client.set(short_code, original_url)


def delete_cached_url(short_code: str):
    if not redis_client:
        return
    redis_client.delete(short_code)