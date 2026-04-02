from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base, get_db
from app import models, schemas, crud, cache
from app.rate_limiter import check_rate_limit

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {"database_status": "ok", "result": value}


@app.get("/redis-health")
def redis_health():
    cache_ping = cache.redis_client.ping()
    return {"redis_status": "ok", "ping": cache_ping}


@app.post("/shorten", response_model=schemas.ShortenResponse)
def shorten_url(
    request: Request,
    body: schemas.ShortenRequest,
    db: Session = Depends(get_db)
):
    check_rate_limit(request)

    db_url = crud.create_short_url(db, body.original_url)

    return {
        "short_code": db_url.short_code,
        "short_url": f"http://127.0.0.1:8000/{db_url.short_code}"
    }


@app.get("/stats/{short_code}", response_model=schemas.StatsResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "short_code": db_url.short_code,
        "original_url": db_url.original_url,
        "click_count": db_url.click_count,
        "created_at": db_url.created_at
    }


@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    cached_url = cache.get_cached_url(short_code)

    if cached_url:
        db_url = crud.get_url_by_code(db, short_code)
        if db_url:
            crud.increment_click_count(db, db_url)
        return RedirectResponse(url=cached_url)

    db_url = crud.get_url_by_code(db, short_code)

    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")

    cache.set_cached_url(short_code, db_url.original_url)
    crud.increment_click_count(db, db_url)

    return RedirectResponse(url=db_url.original_url)