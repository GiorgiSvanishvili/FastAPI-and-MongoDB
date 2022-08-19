import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_URL: str = os.environ["MONGODB_URl"]

    class Config:
        env_file = ".env"


settings = Settings()

