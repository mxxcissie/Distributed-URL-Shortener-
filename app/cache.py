import redis
import logging
from app.config import REDIS_URL

logger = logging.getLogger(__name__)

redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception:
        logger.warning("Redis unavailable, running without cache")
        redis_client = None


def get_cached_url(short_code: str):
    if not redis_client:
        return None
    try:
        return redis_client.get(f"url:{short_code}")
    except Exception:
        return None


def set_cached_url(short_code: str, original_url: str):
    if not redis_client:
        return
    try:
        redis_client.set(f"url:{short_code}", original_url, ex=3600)
    except Exception:
        pass


def delete_cached_url(short_code: str):
    if not redis_client:
        return
    try:
        redis_client.delete(f"url:{short_code}")
    except Exception:
        pass