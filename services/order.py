from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime
from beanie.exceptions import DocumentNotFound


class Order(Document):
    name: str
    # 每个菜品实际价格
    dishes_id: list
    total_price: float
    # 订单状态：已创建、已支付、已接单、已完成、已取消
    status: str
    kitchen_id: PydanticObjectId
    customer_id: PydanticObjectId
    created_at: datetime
    update_at: datetime
    
    class Settings:
        collection = "Order"
        
    def to_dict(self):
        d = {}
        for k, v in self.dict().items():
            # convert ObjectId to str
            if type(v) == PydanticObjectId:
                d[k] = str(v)
            else:
                d[k] = v
        return d

# 实现CRUD
async def create_order(values: dict) -> Order:
    order = Order(**values)
    order_ = await order.insert()
    return order_

async def get_order_by_id(id: PydanticObjectId) -> Order:
    order = await Order.get(id)
    return order

async def update_order(id: PydanticObjectId, values: dict) -> Order:
    order_ = await get_order_by_id(id)
    if not order_:
        raise DocumentNotFound
    for key, value in values.items():
        setattr(order_, key, value)
    await order_.save()

async def delete_order(id: PydanticObjectId) -> None:
    order = await get_order_by_id(id)
    if not order:
        raise DocumentNotFound
    await order.delete()

async def get_orders_by_customer_id(customer_id: PydanticObjectId) -> list[Order]:
    orders = await Order.find(Order.customer_id == customer_id).to_list()
    return orders

