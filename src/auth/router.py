from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy

from src.auth.exceptions import UserIncorrectPasswordError
from src.auth.schemas import Token, UserRegister
from src.auth.utils import authenticate_user, create_access_token, get_password_hash
from src.config import settings
from src.exceptions import DatabaseElementNotFoundError
from src.users.crud import add_new_user


auth_router = APIRouter(tags=['Authentication'], prefix='/auth')


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
