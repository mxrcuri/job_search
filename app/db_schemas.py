from pydantic import BaseModel
from datetime import datetime


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str | None
    description: str | None
    url: str
    source: str | None
    posted_date: datetime | None
    scraped_at: datetime

    class Config:
        from_attributes = True
