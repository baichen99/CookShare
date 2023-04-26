from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from services.admin import Admin
from services.student import Student
from passlib.context import CryptContext


hash_helper = CryptContext(schemes=["bcrypt"])

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
                      document_models=[Admin, Student])
    await init_user()

async def init_user():
    # check if admin exists
    admin = await Admin.find_one(Admin.username == "superadmin")
    if not admin:
        hashed_password = hash_helper.hash("password")
        admin = Admin(username="superadmin", email="admin@example.com", password=hashed_password)
        await admin.insert()
    
    # create students
    for i in range(20):
        password = hash_helper.hash(f"password{i}")
        student = await Student.find_one(Student.username == f"student{i}")
        if student:
            continue
        student = Student(username=f"student{i}", email=f"student{i}@example.com", password=password)
        await student.insert()
        