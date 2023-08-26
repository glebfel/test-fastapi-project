from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import UserIncorrectPasswordError
from src.config import settings
from src.users.crud import get_user_by_email
from src.users.models import User


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm='HS256')


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not verify_password(password, user.hashed_password):
        raise UserIncorrectPasswordError(msg='Incorrect password')
    return user
