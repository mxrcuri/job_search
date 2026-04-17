from pydantic import BaseModel, EmailStr
from datetime import datetime, date

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str | None
    description: str | None
    url: str
    source: str | None
    job_type: str | None
    deadline: date | None
    posted_date: datetime | None
    scraped_at: datetime

    class Config:
        from_attributes = True
