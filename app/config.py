import os

ENV = os.getenv("ENV", "development")

INSTANCE_NAME = os.getenv("INSTANCE_NAME", "unknown-instance")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    if ENV == "development":
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/urlshortener"
    else:
        raise RuntimeError("DATABASE_URL must be set")

REDIS_URL = os.getenv("REDIS_URL")

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

PORT = int(os.getenv("PORT", "8000"))