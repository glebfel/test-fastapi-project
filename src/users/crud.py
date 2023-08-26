from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import DatabaseElementNotFoundError
from src.users.models import User


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    if not (user := (await db.execute(select(User).filter_by(email=email))).scalars().first()):
        raise DatabaseElementNotFoundError(f"User with email '{email}' not found")
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    if not (user := (await db.execute(select(User).filter_by(user_id=user_id))).scalars().first()):
        raise DatabaseElementNotFoundError(f"User with id '{user_id}' not found")
    return user


async def get_users_by_firstname(db: AsyncSession, first_name: str) -> list[User]:
    if not (user := (await db.execute(select(User).filter_by(first_name=first_name.capitalize()))).scalars().all()):
        raise DatabaseElementNotFoundError(f"Users with firstname '{first_name}' not found")
    return user


async def get_all_users(db: AsyncSession) -> list[User]:
    return (await db.execute(select(User))).scalars().all()


async def add_new_user(
    db: AsyncSession, first_name: str, last_name, email: str, username: str, hashed_password: str
) -> User:
    user = User(
        first_name=first_name, last_name=last_name, username=username, email=email, hashed_password=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def update_user_by_id(db: AsyncSession, user_id: int, **kwargs):
    await db.execute(update(User).filter_by(user_id=user_id).values(**kwargs))
    await db.commit()


async def delete_user_by_id(db: AsyncSession, user_id: int):
    await db.execute(delete(User).filter_by(user_id=user_id))
    await db.commit()
