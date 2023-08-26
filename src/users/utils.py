from functools import wraps

from fastapi import HTTPException
from starlette import status

from src.exceptions import DatabaseElementNotFoundError
from src.users.crud import get_user_by_id


def check_user_exists_decorator(func):
    @wraps(func)
    async def wrapper(user_id, **kwargs):
        try:
            await get_user_by_id(user_id)
            return await func(user_id, **kwargs)
        except DatabaseElementNotFoundError as ex:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)

    return wrapper
