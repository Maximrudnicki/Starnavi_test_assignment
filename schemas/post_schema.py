from pydantic import BaseModel
from datetime import datetime


class PostCreate(BaseModel):
    title: str | None = None
    text: str

    class Config:
        from_attributes = True


class PostUpdate(BaseModel):
    title: str | None = None
    text: str | None = None

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    title: str | None
    text: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
