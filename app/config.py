import os

ENV = os.getenv("ENV", "development")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/urlshortener"
)


REDIS_URL = os.getenv("REDIS_URL")


BASE_URL = os.getenv(
    "BASE_URL",
    "http://127.0.0.1:8000"
)

PORT = int(os.getenv("PORT", "8000"))