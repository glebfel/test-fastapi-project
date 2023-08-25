import pathlib

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# root directory
ROOT_PATH = str(pathlib.Path(__file__).parent.parent.parent)


class Settings(BaseSettings):
    # for api
    API_HOST: str = Field(default='0.0.0.0', env='API_HOST')
    # api auth settings
    AUTH_SECRET_KEY: str = Field(..., env="AUTH_SECRET_KEY")
    ALGORITHM: str = Field(default='HS256', env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = '../.env'
        env_file_encoding = 'utf-8'


# load env from file
load_dotenv()

# load vars to settings
settings = Settings()
