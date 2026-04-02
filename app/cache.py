import redis
from app.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def get_cached_url(short_code: str):
    return redis_client.get(short_code)


def set_cached_url(short_code: str, original_url: str):
    redis_client.set(short_code, original_url)