from sqlalchemy.orm import Session
from app import models
from app.utils import generate_short_code


def create_short_url(db: Session, original_url: str):
    short_code = generate_short_code()

    while db.query(models.URL).filter(models.URL.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = models.URL(
        original_url=str(original_url),
        short_code=short_code
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url