from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn as uvicorn

from auth.router import auth_router
from config import settings
from src.database import Base, engine
from src.users.router import user_router


# init database
Base.metadata.create_all(bind=engine)

# init fastapi app
app = FastAPI(title='Test API', version='0.0.1')
app.include_router(auth_router)
app.include_router(user_router)

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.API_HOST, port=8180)
