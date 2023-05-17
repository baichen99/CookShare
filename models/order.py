from pydantic import BaseModel, Field
from typing import Optional
from models.common import SortOrder
from beanie import PydanticObjectId
from datetime import datetime


class OrderCreate(BaseModel):
    name: str = Field("订单", min_length=3, max_length=50)
    # 每个菜品实际价格
    dishes_id: list[PydanticObjectId] = []
    # 订单状态：已创建、已支付、已接单、已完成、已取消
    status: str
    kitchen_id: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "订单",
                "dishes": ["5f760a7e9b3e9c1e3f0e3e1a", "5f760a7e9b3e9c1e3f0e3e1a"],
                "status": "已创建",
                "kitchen_id": "5f760a7e9b3e9c1e3f0e3e1a",
                "customer_id": "5f760a7e9b3e9c1e3f0e3e1a",
                "create_at": "2020-10-01 00:00:00",
                "update_at": "2020-10-01 00:00:00",
            }
        }

class OrderResponse(BaseModel):
    name: str
    name: str
    # dish_price: dict
    dishes_id: list[PydanticObjectId]
    # 订单状态：已创建、已支付、已接单、已完成、已取消
    status: str
    kitchen_id: PydanticObjectId
    customer_id: PydanticObjectId
    created_at: datetime
    update_at: datetime
    
class OrderListResponse(BaseModel):
    skip: int
    limit: int
    total: int
    orders: list[OrderResponse]
    

class OrderUpdate(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=50)
    # dish_price: Optional[dict[PydanticObjectId, float]]
    # 订单状态：已创建、已支付、已接单、已完成、已取消
    status: Optional[str]
    update_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "订单",
                "dish_price": {
                    "菜品1": 10.0,
                    "菜品2": 20.0,
                    "菜品3": 30.0,
                },
                "other_price": {
                    "服务费": 10.0,
                    "清洁费": 20.0,
                },
                "total_price": 70.0,
                "status": "已创建",
                "kitchen_id": "5f760a7e9b3e9c1e3f0e3e1a",
                "customer_id": "5f760a7e9b3e9c1e3f0e3e1a",
                "create_at": "2020-10-01 00:00:00",
                "update_at": "2020-10-01 00:00:00",
            }
        }
    
# class OrderQuery(BaseModel):
#     name: Optional[str]
#     dish_price: Optional[dict[PydanticObjectId, float]]
#     # 每个菜品实际价格
#     dish_price: Optional[dict[PydanticObjectId, float]] = {}
#     # 服务费、清洁费等
#     other_price: Optional[dict[str, float]] = {}
#     total_price: Optional[float] = 0.0
#     # 订单状态：已创建、已支付、已接单、已完成、已取消
#     status: Optional[str]
#     created_at: Optional[datetime]
#     update_at: Optional[datetime]
#     sort_by: Optional[str] = "created_at"
#     sort: Optional[SortOrder] = SortOrder.asc
 