from functools import wraps

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.exceptions import DatabaseElementNotFoundError
from src.users.crud import get_user_by_id


def check_user_exists_decorator(func):
    @wraps(func)
    async def wrapper(db: AsyncSession, user_id: int, **kwargs):
        try:
            await get_user_by_id(db=db, user_id=user_id)
            return await func(db=db, user_id=user_id, **kwargs)
        except DatabaseElementNotFoundError as ex:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)

    return wrapper
