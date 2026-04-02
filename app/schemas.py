from pydantic import BaseModel, HttpUrl
from datetime import datetime


class ShortenRequest(BaseModel):
    original_url: HttpUrl


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str


class StatsResponse(BaseModel):
    short_code: str
    original_url: str
    click_count: int
    created_at: datetime