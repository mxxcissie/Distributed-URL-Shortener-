from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base, get_db
from app import models, schemas, crud

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


@app.post("/shorten", response_model=schemas.ShortenResponse)
def shorten_url(request: schemas.ShortenRequest, db: Session = Depends(get_db)):
    db_url = crud.create_short_url(db, request.original_url)

    return {
        "short_code": db_url.short_code,
        "short_url": f"http://127.0.0.1:8000/{db_url.short_code}"
    }