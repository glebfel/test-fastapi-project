from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


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
