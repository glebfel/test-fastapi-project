from functools import wraps

from fastapi import HTTPException
from starlette import status

from src.exceptions import DatabaseElementNotFoundError


def common_error_handler_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DatabaseElementNotFoundError as ex:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ex.msg)

    return wrapper
