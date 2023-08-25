from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
import sqlalchemy

from auth.exceptions import UserIncorrectPasswordError
from src.auth.schemas import Token, UserRegister
from src.config import settings
from src.exceptions import DatabaseElementNotFoundError
from src.users.crud import add_new_user, get_user_by_email
from src.users.models import User


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

auth_router = APIRouter(tags=['Authentication'], prefix='/auth')


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm='HS256')


def authenticate_user(email: str, password: str) -> User | None:
    user = get_user_by_email(email)
    if not verify_password(password, user.hashed_password):
        raise UserIncorrectPasswordError(msg='Incorrect password')
    return user


@auth_router.post('/register')
def register_user(user: UserRegister) -> Token:
    # check if user already in db
    try:
        add_new_user(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            hashed_password=get_password_hash(user.password),
        )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'username': user.username, 'email': user.email, 'exp': datetime.utcnow() + access_token_expires},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type='bearer', expire=datetime.utcnow() + access_token_expires)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')


@auth_router.post('/login')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except DatabaseElementNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.msg)
    except UserIncorrectPasswordError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.msg)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'username': user.username, 'email': user.email, 'exp': datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer', expire=datetime.utcnow() + access_token_expires)
