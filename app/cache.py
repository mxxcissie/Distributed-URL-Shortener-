import redis
import logging
from app.config import REDIS_URL

logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = 3600

redis_client = None

if REDIS_URL:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.warning("Redis unavailable, running without cache: %s", e)
        redis_client = None


def _key(short_code: str):
    return f"url:{short_code}"


def get_cached_url(short_code: str):
    if not redis_client:
        return None
    try:
        return redis_client.get(_key(short_code))
    except Exception as e:
        logger.warning("Cache get failed: %s", e)
        return None


def set_cached_url(short_code: str, original_url: str):
    if not redis_client:
        return
    try:
        redis_client.set(_key(short_code), original_url, ex=CACHE_TTL_SECONDS)
    except Exception as e:
        logger.warning("Cache set failed: %s", e)


def delete_cached_url(short_code: str):
    if not redis_client:
        return
    try:
        redis_client.delete(_key(short_code))
    except Exception as e:
        logger.warning("Cache delete failed: %s", e)