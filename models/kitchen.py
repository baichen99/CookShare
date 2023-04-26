from pydantic import BaseModel, Field
from typing import Optional, List
from models.common import Order


class KitchenCreate(BaseModel):
    name: str = Field("", min_length=3, max_length=50)
    description: str = Field("", min_length=5, max_length=1000)
    address: Optional[str] = None
    facilities: List[str] = []

    class Config:
        schema_extra = {
            "example": {
                "name": "东北大饭堂",
                "description": "你能在这里吃到最正宗的东北菜",
                "address": "上海市宝山区大场镇xxx",
                "facilities": ["一次性餐具", "餐桌"],
                "owner_id": "5f4d4f4c4e4f4f4d4f4d4f4d"
            }
        }

class KitchenResponse(BaseModel):
    id: str
    name: str
    description: str
    address: Optional[str]
    facilities: List[str] = []
    owner_id: str
    
class KitchenListResponse(BaseModel):
    skip: int
    limit: int
    total: int
    kitchens: List[KitchenResponse]

class KitchenQuery(BaseModel):
    skip: int = 0
    limit: int = 10
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    facilities: Optional[str] = None
    owner_id: Optional[str] = None
    sort_by: str = "name"
    order: Order = Order.asc