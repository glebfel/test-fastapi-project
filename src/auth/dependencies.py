import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_session
from src.exceptions import DatabaseElementNotFoundError
from src.users.crud import get_user_by_email
from src.users.schemas import UserInfo


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login', scheme_name='JWT')


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)) -> UserInfo:
    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get('email')
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        # check expiration date of the token
        if payload.get('exp') and datetime.datetime.fromtimestamp(payload.get('exp')) < datetime.datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expired',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        # check if user with given email in db
        return await get_user_by_email(db, email)
    except DatabaseElementNotFoundError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=ex.msg)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
