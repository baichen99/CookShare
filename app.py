from fastapi import FastAPI
from routes.admin import router as admin_router
from config.config import initiate_database

app = FastAPI()


@app.on_event("startup")
async def start_database():
    await initiate_database()



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}

app.include_router(admin_router, prefix="/admin", tags=["Admin"])