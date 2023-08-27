from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth.dependencies import get_current_user
from src.database import get_session
from src.users.crud import delete_user_by_id as delete_user_by_id_db
from src.users.crud import get_all_users, get_user_by_id, get_users_by_firstname, update_user_by_id
from src.users.schemas import OrderBy, UpdateUserInfo, UserInfo
from src.users.utils import check_user_exists_decorator
from src.utils import common_error_handler_decorator


user_router = APIRouter(tags=['Users'], prefix='/users', dependencies=[Depends(get_current_user)])


@user_router.get('/info/{user_id}')
@common_error_handler_decorator
async def get_user_info_by_id(user_id: int, db: AsyncSession = Depends(get_session)) -> UserInfo:
    """Get user info by id"""
    return await get_user_by_id(db, user_id)


@user_router.get('/search/{first_name}')
@common_error_handler_decorator
async def get_users_info_by_firstname(first_name: str, db: AsyncSession = Depends(get_session)) -> list[UserInfo]:
    """Get user info by firstname
    (can be more than one user because firstname is not unique field)"""
    return await get_users_by_firstname(db, first_name)


@user_router.get('/all')
@common_error_handler_decorator
async def get_all_users_info(
    order_by: OrderBy = OrderBy.user_id,
    is_desc_sort: bool = False,
    filters: str = None,
    db: AsyncSession = Depends(get_session),
) -> list[UserInfo]:
    """Get all users info"""
    try:
        filters_criteria = {}
        # filter
        if filters is not None:
            filters_criteria = dict(x.strip().split('=') for x in filters.split(','))
            # check if all keys are in user model attrs
            for attr in filters_criteria.keys():
                if attr not in UserInfo.model_fields.keys():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid filter input: attribute '{attr}' doesn't exist in UserInfo model",
                    )
        return await get_all_users(filters_criteria, order_by, is_desc_sort, db)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid filter input: valid format - attr1=value1,attr2=value2,...',
        )


@user_router.put('/update/{user_id}')
@check_user_exists_decorator
async def update_user_info_by_id(user_id: int, user_info: UpdateUserInfo, db: AsyncSession = Depends(get_session)):
    """Update user info by id"""
    updatable_fields = {}
    for i in user_info.model_dump():
        if user_info.model_dump()[i]:
            updatable_fields.update({i: user_info.model_dump()[i]})
    await update_user_by_id(db, user_id, **updatable_fields)
    return {'status': 'success', 'message': f"User with id='{user_id}' was successfully updated"}


@user_router.delete('/delete/{user_id}')
@check_user_exists_decorator
async def delete_user_by_id(user_id: int, db: AsyncSession = Depends(get_session)):
    """Update user info by id"""
    await delete_user_by_id_db(db, user_id)
    return {'status': 'success', 'message': f"User with id='{user_id}' id deleted"}
