from sqlalchemy import select

from src.database import async_session
from src.exceptions import DatabaseElementNotFoundError
from src.users.models import User


async def get_user_by_email(email: str) -> User:
    async with async_session() as session:
        if not (user := (await session.execute(select(User).filter_by(email=email))).scalars().first()):
            raise DatabaseElementNotFoundError(f"User with email '{email}' not found")
        return user


async def get_user_by_id(user_id: int) -> User:
    async with async_session() as session:
        if not (user := (await session.execute(select(User).filter_by(user_id=user_id))).scalars().first()):
            raise DatabaseElementNotFoundError(f"User with id '{user_id}' not found")
        return user


async def get_users_by_firstname(firstname: str) -> list[User]:
    async with async_session() as session:
        if not (user := (await session.execute(select(User).filter_by(firstname=firstname))).scalars().all()):
            raise DatabaseElementNotFoundError(f"Users with firstname '{firstname}' not found")
        return user


async def get_all_users() -> list[User]:
    async with async_session() as session:
        return (await session.execute(select(User))).scalars().all()


async def add_new_user(first_name: str, last_name, email: str, username: str, hashed_password: str) -> User:
    async with async_session() as session:
        user = User(
            first_name=first_name, last_name=last_name, username=username, email=email, hashed_password=hashed_password
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def update_user_by_id(user_id: int, **kwargs):
    async with async_session() as session:
        await session.execute(select(User).filter_by(user_id=user_id).update(kwargs))
        await session.commit()


async def delete_user_by_id(user_id: int):
    async with async_session() as session:
        await session.execute(select(User).filter_by(user_id=user_id).delete())
        await session.commit()
