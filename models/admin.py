from pydantic import BaseModel, EmailStr

class Admin(BaseModel):
    username: str
    email: EmailStr
    password: str

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "email": "example@example.com",
                "password": "password"
            }
        }

class AdminSignIn(BaseModel):
    email: EmailStr
    password: str

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "password"
            }
        }
        
class AdminResponse(BaseModel):
    email: EmailStr
    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "email": "admin",
            }
        }