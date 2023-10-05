"""
# Pydantic models - schemas for all api responses and post requests
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    user_id: Optional[int] = None


class Response(Post):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BaseUser(BaseModel):
    email: EmailStr


class UserPost(BaseUser):
    password: str


class UserRequest(BaseUser):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
