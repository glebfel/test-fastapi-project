from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import auth_router
from src.database import Base, engine
from src.users.router import user_router


# init database
@asynccontextmanager
async def init_tables(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield


# init fastapi app
app = FastAPI(title='Test API', version='0.0.1', lifespan=init_tables)
app.include_router(auth_router)
app.include_router(user_router)

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
