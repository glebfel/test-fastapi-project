from dotenv import load_dotenv
from pydantic import Extra, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # api auth settings
    AUTH_SECRET_KEY: str = Field(..., env='AUTH_SECRET_KEY')
    ALGORITHM: str = Field(default='HS256', env='ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env='ACCESS_TOKEN_EXPIRE_MINUTES')

    class Config:
        env_prefix = ''
        case_sentive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow


# load env from file
load_dotenv()

# load vars to settings
settings = Settings()
