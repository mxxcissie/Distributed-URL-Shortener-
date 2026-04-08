from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)

    short_code = Column(String(10), unique=True, index=True, nullable=False)

    original_url = Column(String(2048), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    click_count = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<URL(short_code={self.short_code}, original_url={self.original_url})>"