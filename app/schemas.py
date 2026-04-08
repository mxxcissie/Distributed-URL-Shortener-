from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


class ShortenRequest(BaseModel):
    original_url: HttpUrl = Field(..., description="The original URL to shorten")

    model_config = {"from_attributes": True}


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str

    model_config = {"from_attributes": True}


class StatsResponse(BaseModel):
    short_code: str
    original_url: str
    click_count: int = Field(..., description="Number of times the short URL was accessed")
    created_at: datetime

    model_config = {"from_attributes": True}