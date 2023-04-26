from typing import Optional, List, Literal
from pydantic import BaseModel, EmailStr, Field
from enum import IntEnum


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "password"
            }
        }

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "email": "user@email.com",
                "password": "password"
            }
        }

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "username": "user",
                "email": "user@mail.com",
            }
        }

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    # 用于OPENAPI文档
    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "email": "user@mail.com",
                "password": "password"
            }
        }

class Order(IntEnum):
    asc = 1
    desc = -1

class UserQuery(BaseModel):
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

class UserListResponse(BaseModel):
    skip: int
    limit: int
    total: int
    users: List[UserResponse]