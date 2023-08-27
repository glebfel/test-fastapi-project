from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import UserIncorrectPasswordError
from src.auth.schemas import Token, UserRegister
from src.auth.utils import authenticate_user, create_access_token, get_password_hash
from src.config import settings
from src.database import get_session
from src.users.crud import add_new_user
from src.utils import common_error_handler_decorator


auth_router = APIRouter(tags=['Authentication'], prefix='/auth')


@auth_router.post('/register')
async def register_user(user: UserRegister, db: AsyncSession = Depends(get_session)) -> Token:
    """Register new user"""
    # check if user already in db
    try:
        await add_new_user(
            db,
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
@common_error_handler_decorator
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)
) -> Token:
    """Authorize registered user"""
    try:
        user = await authenticate_user(db, form_data.username, form_data.password)
    except UserIncorrectPasswordError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.msg)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'username': user.username, 'email': user.email, 'exp': datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type='bearer', expire=datetime.utcnow() + access_token_expires)
