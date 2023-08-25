import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.router import auth_router
from config import settings
from src.database import Base, engine

# init database
Base.metadata.create_all(bind=engine)

# init fastapi app
app = FastAPI(title='Test API', version='0.0.1')
app.include_router(auth_router)

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.API_HOST, port=8180)