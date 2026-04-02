import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/urlshortener"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0"
)