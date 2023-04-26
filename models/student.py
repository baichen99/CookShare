from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field
from enum import IntEnum


class StudentLogin(BaseModel):
    email: EmailStr
    password: str

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "email": "student@example.com",
                "password": "password"
            }
        }

class StudentRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "username": "student",
                "email": "user@email.com",
                "password": "password"
            }
        }

class StudentResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "username": "student",
                "email": "student@mail.com",
            }
        }

class StudentUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "username": "student",
                "email": "student@mail.com",
                "password": "password"
            }
        }

class Order(IntEnum):
    asc = 1
    desc = -1

class StudentQuery(BaseModel):
    skip: int = 1
    limit: int = Field(ge=1, le=100, default=10)
    sort_by: str = "email"
    order: Order = Order.asc
    username: Optional[str]
    email: Optional[EmailStr]
    class Config:
        schema_extra = {
            "example": ""
        }

class StudentListResponse(BaseModel):
    skip: int
    limit: int
    total: int
    students: List[StudentResponse]
