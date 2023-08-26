import asyncio

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.auth.dependencies import get_current_user
from src.auth.utils import get_password_hash
from src.database import Base, get_session
from src.main import app
from src.users.models import User


TEST_DATABASE_URL = 'sqlite+aiosqlite:///./test.db'

engine = create_async_engine(TEST_DATABASE_URL)

test_async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_test_user_data() -> list[User]:
    return [
        User(
            user_id=1,
            first_name='Roger',
            last_name='Smith',
            username='rog123',
            email='rogersm1@gmail.com',
            hashed_password=get_password_hash('123'),
        ),
        User(
            user_id=2,
            first_name='Alice',
            last_name='Jane',
            username='alice_jane_2000',
            email='alice2000@yahoo.com',
            hashed_password=get_password_hash('alice1!'),
        ),
    ]


# override db session
async def override_get_session() -> AsyncSession:
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


# override auth process
async def override_get_current_user():
    pass


app.dependency_overrides[get_current_user] = override_get_current_user


# init test db
async def init_models():
    async with engine.begin() as conn:
        async with test_async_session() as session:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            session.add_all(get_test_user_data())
            await session.commit()


asyncio.run(init_models())


@pytest.fixture
def client():
    return TestClient(app)
