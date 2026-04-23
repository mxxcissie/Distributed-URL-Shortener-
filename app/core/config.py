import os
from typing import List, Optional


def parse_csv_env(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_bool_env(value: Optional[str], default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


ENV = os.getenv("ENV", "development")

INSTANCE_NAME = os.getenv("INSTANCE_NAME", "unknown-instance")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    if ENV in ("development", "test"):
        DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/urlshortener"
    else:
        raise RuntimeError("DATABASE_URL must be set")

REDIS_URL = os.getenv("REDIS_URL")

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

PORT = int(os.getenv("PORT", "8000"))

CORS_ALLOW_ORIGINS = parse_csv_env(
    os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost:5173,https://url-shortener-frontend-av1x.onrender.com",
    )
)

AUTO_CREATE_SCHEMA = parse_bool_env(
    os.getenv("AUTO_CREATE_SCHEMA"),
    default=ENV in ("development", "test"),
)
