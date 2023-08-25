from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from src.users.models import User


class UpdateUserInfo(BaseModel):
    first_name: str = Field(max_length=30, default=None)
    last_name: str = Field(max_length=30, default=None)
    username: str = Field(max_length=30, default=None)


class UserInfo(UpdateUserInfo):
    user_id: int
    email: EmailStr
    registered_at: datetime

    @classmethod
    def marshal(cls, model: User) -> UserInfo:
        return cls(
            user_id=model.user_id,
            first_name=model.first_name,
            last_name=model.last_name,
            username=model.username,
            email=model.email,
            registered_at=model.registered_at,
        )
