from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, EmailStr, Field


class OrderBy(StrEnum):
    user_id = 'user_id'
    email = 'email'
    first_name = 'first_name'
    last_name = 'last_name'
    username = 'username'
    registered_at = 'registered_at'


class UpdateUserInfo(BaseModel):
    first_name: str = Field(max_length=30, default=None)
    last_name: str = Field(max_length=30, default=None)
    username: str = Field(max_length=30, default=None)


class UserInfo(UpdateUserInfo):
    user_id: int
    email: EmailStr
    registered_at: datetime

    class Config:
        from_attributes = True
