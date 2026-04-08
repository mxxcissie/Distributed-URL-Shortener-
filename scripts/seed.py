from sqlalchemy.orm import Session
import logging
from app.database import SessionLocal, engine, Base
from app.models import URL

logger = logging.getLogger(__name__)


def seed_data():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    sample_urls = [
        {"short_code": "abc123", "original_url": "https://www.google.com/", "click_count": 0},
        {"short_code": "xyz789", "original_url": "https://www.github.com/", "click_count": 0},
        {"short_code": "demo01", "original_url": "https://www.python.org/", "click_count": 0},
    ]

    try:
        for item in sample_urls:
            existing = db.query(URL).filter(URL.short_code == item["short_code"]).first()
            if not existing:
                db_url = URL(**item)
                db.add(db_url)

        db.commit()
        logger.info("Seed data inserted successfully.")

    except Exception as e:
        db.rollback()
        logger.error("Seeding failed: %s", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()