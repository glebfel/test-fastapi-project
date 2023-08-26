import pytest

from src.auth.utils import get_password_hash
from src.exceptions import DatabaseElementNotFoundError
from src.users.crud import (
    add_new_user,
    delete_user_by_id,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    get_users_by_firstname,
    update_user_by_id,
)
from tests.conftest import get_test_user_data, test_async_session


@pytest.fixture
def db_session():
    return test_async_session()


@pytest.mark.asyncio
async def test_get_use_by_id(db_session):
    db_response = await get_user_by_id(db_session, 1)
    assert db_response.user_id == get_test_user_data()[0].user_id


@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
    db_response = await get_user_by_email(db_session, get_test_user_data()[1].email)
    assert db_response.email == get_test_user_data()[1].email


@pytest.mark.asyncio
async def test_get_users_by_firstname(db_session):
    db_response = await get_users_by_firstname(db_session, get_test_user_data()[1].first_name)
    assert db_response[0].first_name == get_test_user_data()[1].first_name


@pytest.mark.asyncio
async def test_get_all_users(db_session):
    db_response = await get_all_users(db_session)
    assert len(db_response) == len(get_test_user_data())


@pytest.mark.asyncio
async def test_add_new_user(db_session):
    await add_new_user(
        db_session,
        first_name='Test',
        last_name='Test',
        username='test',
        email='test@mail.ru',
        hashed_password=get_password_hash('test'),
    )
    db_response = await get_all_users(db_session)
    assert len(db_response) == len(get_test_user_data()) + 1


@pytest.mark.asyncio
async def test_update_user_by_id(db_session):
    new_username = 'new'
    await update_user_by_id(db_session, user_id=1, username=new_username)
    db_response = await get_user_by_id(db_session, 1)
    assert db_response.username == new_username


@pytest.mark.asyncio
async def test_delete_user_by_id(db_session):
    await delete_user_by_id(db_session, user_id=1)
    try:
        await get_user_by_id(db_session, 1)
    except DatabaseElementNotFoundError:
        assert True
