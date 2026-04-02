from fastapi import FastAPI
from sqlalchemy import text
from app.database import engine

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db-health")
def db_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar()

    return {"database_status": "ok", "result": value}