from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.admin import router as admin_router
from routes.user import router as user_router
from routes.kitchen import router as kitchen_router
from routes.dish import router as dish_router
from config.config import initiate_database
from middlewares.error_handler import JSONException


def create_app():
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
    
    @app.on_event("startup")
    async def start_database():
        await initiate_database()
    return app

app = create_app()

