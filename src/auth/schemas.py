from datetime import datetime
from typing import Annotated

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime


class UserRegister(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    email: EmailStr
    password: str


class CustomOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        email: Annotated[str, Form()],
        password: Annotated[str, Form()],
    ):
        super().__init__(username=email, password=password)
