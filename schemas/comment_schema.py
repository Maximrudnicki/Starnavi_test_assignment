from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CommentCreate(BaseModel):
    post_id: int
    text: str

    class Config:
        from_attributes = True


class CommentUpdate(BaseModel):
    text: Optional[str] | None = None
    is_banned: Optional[bool] | None = None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    text: str
    is_banned: Optional[bool] = False
    created_at: datetime

    class Config:
        from_attributes = True
