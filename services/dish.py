from beanie import Document
from beanie import PydanticObjectId
from datetime import datetime
from beanie.exceptions import DocumentNotFound
from models.dish import DishQuery
from pydantic import Field
from typing import Optional


class Dish(Document):
    name: str
    description: str
    price: float
    image: Optional[str]
    kitchen_id: PydanticObjectId
    creator_id: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        collection = "dish"
        
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
async def create_dish(values: dict) -> Dish:
    dish = Dish(**values)
    return await dish.insert()

async def get_dish_by_id(id: PydanticObjectId) -> Dish:
    dish = await Dish.get(id)
    return dish

async def update_dish(id: PydanticObjectId, values: dict) -> Dish:
    dish_ = await get_dish_by_id(id)
    if not dish_:
        raise DocumentNotFound
    for key, value in values.items():
        setattr(dish_, key, value)
    dish_.update_at = datetime.utcnow()
    await dish_.save()
    return dish_

async def delete_dish(id: PydanticObjectId) -> None:
    dish = await get_dish_by_id(id)
    if not dish:
        raise DocumentNotFound
    await dish.delete()
    return dish

async def get_dishes_by_kitchen_id(kitchen_id: PydanticObjectId) -> list[Dish]:
    dishes = await Dish.find(Dish.kitchen_id == kitchen_id).to_list()
    return dishes

async def get_dishes(query: DishQuery) -> list[Dish]:
    query_list = []
    if query.name:
        query_list.append(Dish.name == query.name)
    if query.kitchen_id:
        query_list.append(Dish.kitchen_id == query.kitchen_id)
    if query.price_min:
        query_list.append(Dish.price >= query.price_min)
    if query.price_max:
        query_list.append(Dish.price <= query.price_max)
    dishes = await Dish.find(*query_list).skip(query.skip).limit(query.limit)\
        .sort((query.sort_by, query.order)).to_list()
    return dishes


