import pytest
from starlette.testclient import TestClient
from config.config import Settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from services.admin import Admin
from services.user import User
from services.kitchen import Kitchen
from services.dish import Dish
from services.order import Order
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from middlewares.error_handler import JSONException
from routes.admin import router as admin_router
from routes.user import router as user_router
from routes.kitchen import router as kitchen_router
from routes.dish import router as dish_router
from routes.order import router as order_router
from passlib.context import CryptContext
import asyncio


hash_helper = CryptContext(schemes=["bcrypt"])


@pytest.fixture(scope="module")
def settings_override():
    return Settings(_env_file=".env.test", _env_file_encoding="utf-8")

@pytest.fixture(scope="module")
def test_app(settings_override):
    # set up
    app = FastAPI()

    @app.exception_handler(JSONException)
    async def Custom_exception_handler(request: Request, exc: JSONException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.error_msg,
                },
        )

    @app.get("/", tags=["Root"])
    async def read_root():
        return {"message": "Welcome to this fantastic app."}

    app.include_router(admin_router, prefix="/admin", tags=["Admin"])
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(kitchen_router, prefix="/kitchen", tags=["Kitchen"])
    app.include_router(dish_router, prefix="/dish", tags=["Dish"])
    app.include_router(order_router, prefix="/order", tags=["Order"])
    
    @app.on_event("startup")
    async def start_database():
        print("Starting database: ", settings_override.MONGO_DB_NAME)
        client = AsyncIOMotorClient(
            host=settings_override.DATABASE_HOST,
            port=settings_override.DATABASE_PORT,
            username=settings_override.MONGO_DB_USER,
            password=settings_override.MONGO_DB_PASSWORD,
            authSource=settings_override.MONGO_DB_NAME,
        )
        # initiate database
        await init_beanie(database=client.get_database(settings_override.MONGO_DB_NAME),
                        document_models=[Admin, User, Kitchen, Dish, Order])
        # create superadmin
        admin = await Admin.find_one(Admin.username == "superadmin")
        if not admin:
            hashed_password = hash_helper.hash("password")
            admin = Admin(username="superadmin", email="admin@example.com", password=hashed_password)
            await admin.insert()

    with TestClient(app) as test_client:
        # testing
        yield test_client
