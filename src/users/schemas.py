from datetime import datetime

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    registered_at: datetime


class UpdateUserInfo(BaseModel):
    first_name: str = Field(max_length=30, default=None)
    last_name: str = Field(max_length=30, default=None)
    username: str = Field(max_length=30, default=None)