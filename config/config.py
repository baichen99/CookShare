from typing import Optional
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings
from services.admin import Admin
from services.user import User
from services.kitchen import Kitchen
from services.dish import Dish
from services.order import Order
from passlib.context import CryptContext
from datetime import datetime


hash_helper = CryptContext(schemes=["bcrypt"])

class Settings(BaseSettings):        
    # database configurations
    DATABASE_HOST: str
    DATABASE_PORT: int
    MONGO_DB_NAME: str
    MONGO_DB_USER: str
    MONGO_DB_PASSWORD: str


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
                      document_models=[Admin, User, Kitchen, Dish, Order])
    await init_user()
    print("Database initiated")
    
async def init_user():
    # check if admin exists
    admin = await Admin.find_one(Admin.username == "superadmin")
    if not admin:
        hashed_password = hash_helper.hash("password")
        admin = Admin(username="superadmin", email="admin@example.com", password=hashed_password)
        await admin.insert()
    
    # create users
    for i in range(20):
        password = hash_helper.hash(f"password{i}")
        user = await User.find_one(User.username == f"user{i}")
        if user:
            continue
        user = User(username=f"user{i}", email=f"user{i}@example.com", password=password)
        await user.insert()

async def init_kitchen():
    # getusers
    users = await User.find_all().to_list()
    
    # create kitchens
    kitchens = [
        {   
            "name": "沙县小吃",
            "description": "各种家常小吃",
            "address": "上海市宝山区上海大学旁边",
            "price": 40.0,
            "facilities": ["wifi", "空调"],
            "available_times": ["11:00-14:00", "17:00-20:00"],
            "owner_id": users[0].id,
            "created_at": "2021-06-04T15:00:00",
            "updated_at": "2021-06-04T15:00:00"
        },
        {
            "name": "快餐快餐",
            "description": "汉堡、薯条、可乐",
            "address": "上海市宝山区上海大学旁边",
            "price": 40.0,
            "facilities": ["wifi", "空调"],
            "available_times": ["11:00-14:00", "17:00-20:00"],
            "owner_id": users[1].id,
            "created_at": "2021-06-04T15:00:00",
        }
    ]
    for kitchen in kitchens:
        if not await Kitchen.find_one(Kitchen.name == kitchen['name']):
            await Kitchen(**kitchen).insert()
    


