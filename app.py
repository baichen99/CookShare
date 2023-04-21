from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.admin import router as admin_router
from config.config import initiate_database
from middlewares.error_handler import JSONException

app = FastAPI()


@app.exception_handler(JSONException)
async def Custom_exception_handler(request: Request, exc: JSONException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.error_msg,
            },
    )

@app.on_event("startup")
async def start_database():
    await initiate_database()



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app."}

app.include_router(admin_router, prefix="/admin", tags=["Admin"])