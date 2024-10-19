from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    auto_reply_enabled: Optional[bool] | None = None
    auto_reply_delay: Optional[int] | None = None

    class Config:
        from_attributes = True
