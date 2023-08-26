from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.users.crud import delete_user_by_id as delete_user_by_id_db
from src.users.crud import get_all_users, get_user_by_id, get_users_by_firstname, update_user_by_id
from src.users.schemas import UpdateUserInfo, UserInfo
from src.users.utils import check_user_exists_decorator
from src.utils import common_error_handler_decorator


user_router = APIRouter(tags=['Users'], prefix='/users')


@user_router.get('/info/{user_id}', dependencies=[Depends(get_current_user)])
@common_error_handler_decorator
async def get_user_info_by_id(user_id: int) -> UserInfo:
    """Get user info by id"""
    return UserInfo.marshal(await get_user_by_id(user_id))


@user_router.get('/all', dependencies=[Depends(get_current_user)])
@common_error_handler_decorator
async def get_all_users_info() -> list[UserInfo]:
    """Get all users info"""
    return [UserInfo.marshal(user) for user in await get_all_users()]


@user_router.get('/info/{firstname}', dependencies=[Depends(get_current_user)])
@common_error_handler_decorator
async def get_users_info_by_firstname(firstname: str) -> list[UserInfo]:
    """Get user info by firstname
    (can be more than one user because firstname is not unique field)"""
    return [UserInfo.marshal(user) for user in await get_users_by_firstname(firstname)]


@user_router.put('/update/{user_id}', dependencies=[Depends(get_current_user)])
@check_user_exists_decorator
async def update_user_info_by_id(user_id: int, user_info: UpdateUserInfo):
    """Update user info by id"""
    updatable_fields = {}
    for i in user_info.model_dump():
        if user_info.model_dump()[i]:
            updatable_fields.update({i: user_info.model_dump()[i]})
    await update_user_by_id(user_id, **updatable_fields)
    return {'status': 'success', 'message': f"User with id='{user_id}' was successfully updated"}


@user_router.delete('/delete/{user_id}', dependencies=[Depends(get_current_user)])
@check_user_exists_decorator
async def delete_user_by_id(user_id: int):
    """Update user info by id"""
    await delete_user_by_id_db(user_id)
    return {'status': 'success', 'message': f"User with id='{user_id}' id deleted"}
