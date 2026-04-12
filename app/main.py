import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base, get_db
from app import schemas, crud
from app.services import cache
from app.services.rate_limiter import check_rate_limit
from app.core.config import BASE_URL, INSTANCE_NAME


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting instance %s", INSTANCE_NAME)
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down instance %s", INSTANCE_NAME)


app = FastAPI(title="URL Shortener API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://url-shortener-frontend-av1x.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000

    logger.info(
        "Instance %s handled %s %s in %.2f ms",
        INSTANCE_NAME,
        request.method,
        request.url.path,
        duration_ms,
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.scalar()
        return {"database_status": "ok", "result": value}
    except Exception as exc:
        logger.exception("Database health check failed")
        raise HTTPException(status_code=500, detail="Database connection failed") from exc


@app.get("/redis-health")
def redis_health():
    if not cache.redis_client:
        return {"redis_status": "not_configured"}

    try:
        cache_ping = cache.redis_client.ping()
        return {"redis_status": "ok", "ping": cache_ping}
    except Exception as exc:
        logger.exception("Redis health check failed")
        raise HTTPException(status_code=500, detail="Redis connection failed") from exc


@app.post("/shorten", response_model=schemas.ShortenResponse)
def shorten_url(
    request: Request,
    body: schemas.ShortenRequest,
    db: Session = Depends(get_db),
):
    check_rate_limit(request)

    try:
        db_url = crud.create_short_url(db, body.original_url)

        logger.info("Created short URL for %s", body.original_url)

        return {
            "short_code": db_url.short_code,
            "short_url": f"{BASE_URL}/{db_url.short_code}",
        }

    except Exception as exc:
        logger.exception("Failed to create short URL")
        raise HTTPException(status_code=500, detail="Failed to create short URL") from exc


@app.get("/stats/{short_code}", response_model=schemas.StatsResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "short_code": db_url.short_code,
        "original_url": db_url.original_url,
        "click_count": db_url.click_count,
        "created_at": db_url.created_at,
    }


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    try:
        cached_url = cache.get_cached_url(short_code)

        if cached_url:
            logger.info("Cache hit for short code %s", short_code)

            db_url = crud.get_url_by_code(db, short_code)
            if db_url:
                crud.increment_click_count(db, db_url)

            return RedirectResponse(url=cached_url)

        logger.info("Cache miss for short code %s", short_code)

        db_url = crud.get_url_by_code(db, short_code)
        if not db_url:
            raise HTTPException(status_code=404, detail="Short URL not found")

        cache.set_cached_url(short_code, db_url.original_url)

        crud.increment_click_count(db, db_url)

        return RedirectResponse(url=db_url.original_url)

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Redirect failed for short code %s", short_code)
        raise HTTPException(status_code=500, detail="Redirect failed") from exc