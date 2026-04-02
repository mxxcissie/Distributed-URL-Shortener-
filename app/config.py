import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/urlshortener"
)

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)