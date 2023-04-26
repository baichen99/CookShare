from pydantic import BaseModel, EmailStr
from typing import List

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

class AdminLogin(BaseModel):
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
    username: str
    email: EmailStr
    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@example.com",
            }
        }
        
class AdminListResponse(BaseModel):
    students: List[AdminResponse]
