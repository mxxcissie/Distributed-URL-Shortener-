from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import models
from app.utils import generate_short_code


def create_short_url(db: Session, original_url: str):
    for _ in range(5):
        short_code = generate_short_code()

        db_url = models.URL(
            original_url=str(original_url),
            short_code=short_code
        )
        db.add(db_url)

        try:
            db.commit()
            db.refresh(db_url)
            return db_url
        except IntegrityError:
            db.rollback()

    raise ValueError("Failed to generate a unique short code after multiple attempts")


def get_url_by_code(db: Session, short_code: str):
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()


def increment_click_count(db: Session, db_url):
    db_url.click_count += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def increment_click_count_by_code(db: Session, short_code: str) -> bool:
    updated_rows = (
        db.query(models.URL)
        .filter(models.URL.short_code == short_code)
        .update(
            {models.URL.click_count: models.URL.click_count + 1},
            synchronize_session=False,
        )
    )
    db.commit()
    return updated_rows > 0
