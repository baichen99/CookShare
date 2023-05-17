from typing import Optional
from beanie import Document
from beanie import PydanticObjectId
from beanie.exceptions import DocumentNotFound
from beanie.operators import Eq, RegEx, All
from models.kitchen import KitchenQuery
from datetime import datetime
from pydantic import Field


class Kitchen(Document):
    name: str
    description: str
    address: str
    price: Optional[int]
    facilities: Optional[list[str]] = []
    available_times: Optional[list[str]] = []
    owner_id: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)

    
    class Settings:
        collection = "kitchen"
        
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
async def create_kitchen(values: dict) -> Kitchen:
    kitchen = Kitchen(**values)
    kitchen_ = await kitchen.insert()
    return kitchen_

async def get_kitchen_by_id(id: PydanticObjectId) -> Kitchen:
    kitchen = await Kitchen.get(id)
    return kitchen

async def update_kitchen(id: PydanticObjectId, values: dict) -> Kitchen:
    kitchen = await get_kitchen_by_id(id)
    if not kitchen:
        raise DocumentNotFound
    for key, value in values.items():
        setattr(kitchen, key, value)
    await kitchen.save()
    # return 201


async def delete_kitchen(id: PydanticObjectId) -> None:
    kitchen = await get_kitchen_by_id(id)
    if not kitchen:
        raise DocumentNotFound
    await kitchen.delete()

async def get_kitchens_by_owner_id(owner_id: PydanticObjectId) -> list[Kitchen]:
    kitchens = await Kitchen.find(Kitchen.owner_id == owner_id).to_list()
    return kitchens

async def get_kitchens(query: KitchenQuery) -> list[Kitchen]:
    query_list = []
    if query.name:
        query_list.append(RegEx(Kitchen.name, query.name))
    if query.description:
        query_list.append(RegEx(Kitchen.description, query.description))
    if query.address:
        query_list.append(RegEx(Kitchen.address, query.address))
    if query.facilities:
        facilities = query.facilities.split(',')
        query_list.append(All(Kitchen.facilities, facilities))
    if query.owner_id:
        query_list.append(Eq(Kitchen.owner_id, PydanticObjectId(query.owner_id)))
    kitchens = await Kitchen.find_many(*query_list).skip(query.skip).limit(query.limit)\
        .sort((query.sort_by, query.order)).to_list()
    return kitchens
