from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from services.admin import Admin


class Settings(BaseSettings):
    # database configurations
    DATABASE_HOST: Optional[str] = None
    DATABASE_PORT: Optional[int] = None
    MONGO_DB_NAME: Optional[str] = None
    MONGO_DB_USER: Optional[str] = None
    MONGO_DB_PASSWORD: Optional[str] = None


    # JWT
    secret_key: str
    algorithm: str = "HS256"

    class Config:
        env_file = ".env.dev"


async def initiate_database():
    client = AsyncIOMotorClient(
        host=Settings().DATABASE_HOST,
        port=Settings().DATABASE_PORT,
        username=Settings().MONGO_DB_USER,
        password=Settings().MONGO_DB_PASSWORD,
        authSource=Settings().MONGO_DB_NAME,
    )
    await init_beanie(database=client.get_database(Settings().MONGO_DB_NAME),
                      document_models=[Admin])