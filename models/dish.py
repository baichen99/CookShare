from pydantic import BaseModel, Field
from typing import Optional
from models.common import SortOrder
from beanie import PydanticObjectId


class DishCreate(BaseModel):
    name: str = Field("", min_length=3, max_length=50)
    description: str = Field("", min_length=5, max_length=1000)
    price: float = Field(0, ge=0)
    image: Optional[str] = None
    kitchen_id: str = Field(min_length=24, max_length=24)
    creator_id: Optional[str] = Field(None, min_length=24, max_length=24)
    class Config:
        schema_extra = {
            "example": {
                "name": "鱼香肉丝",
                "description": "鱼香肉丝是一道汉族传统名菜，属于川菜系。",
                "price": 20.0,
                "image": "https://img.alicdn.com/imgextra/i4/725677994/O1CN01QYQ4QI1QJZ1Y9YQ8Y_!!725677994.jpg",
                "kitchen_id": "5f4d4f4c4e4f4f4d4f4d4f4d"
            }
        }

class DishUpdate(BaseModel):
    name: str = Field("", min_length=3, max_length=50)
    description: str = Field("", min_length=5, max_length=1000)
    price: float = Field(0, ge=0)
    image: Optional[str] = None
    class Config:
        schema_extra = {
            "example": {
                "name": "鱼香肉丝",
                "description": "鱼香肉丝是一道汉族传统名菜，属于川菜系。",
                "price": 20.0,
                "image": "https://img.alicdn.com/imgextra/i4/725677994/O1CN01QYQ4QI1QJZ1Y9YQ8Y_!!725677994.jpg",
            }
        }
   
class DishResponse(BaseModel):
    id: PydanticObjectId
    name: str
    description: str
    price: float
    image: Optional[str]
    kitchen_id: PydanticObjectId
    creator_id: PydanticObjectId

    class Config:
        schema_extra = {
            "example": {
                "id": "5f4d4f4c4e4f4f4d4f4d4f4d",
                "name": "鱼香肉丝",
                "description": "鱼香肉丝是一道汉族传统名菜，属于川菜系。",
                "price": 20.0,
                "image": "https://img.alicdn.com/imgextra/i4/725677994/O1CN01QYQ4QI1QJZ1Y9YQ8Y_!!725677994.jpg",
                "kitchen_id": "5f4d4f4c4e4f4f4d4f4d4f4d",
                "creator_id": "5f4d4f4c4e4f4f4d4f4d4f4d"
            }
        }
    
class DishListResponse(BaseModel):
    skip: int
    limit: int
    total: int
    dishes: list[DishResponse]

class DishQuery(BaseModel):
    skip: int = 0
    limit: int = 10
    name: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    kitchen_id: Optional[str] = None
    sort_by: str = "name"
    order: SortOrder = SortOrder.asc