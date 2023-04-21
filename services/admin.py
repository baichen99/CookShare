from typing import Optional, List
from beanie import Document, Indexed
from beanie import PydanticObjectId


class Admin(Document):
    username: str
    email: str
    password: str

    class Settings:
        collection = "admin"


async def get_admin_by_id(id: PydanticObjectId):
    admin = await Admin.find_one(Admin.id == id)
    return admin

async def get_admin_by_email(email: str):
    admin = await Admin.find_one(Admin.email == email)
    return admin

async def get_admins(skip: int = 0, limit: int = 100, sort_by: str = "email", order: str = "asc") -> List[Admin]:
    admins = await Admin.find().skip(skip).limit(limit).sort(sort_by, order).to_list()
    return admins

async def create_admin(admin: Admin) -> Admin:
    admin_ = await admin.create()
    return admin_

async def update_admin(id: PydanticObjectId, admin: Admin) -> Admin:
    admin_ = await Admin.find_one(Admin.id == id)
    values = admin.dict(exclude_unset=True)
    for key, value in values.items():
        setattr(admin_, key, value)
    await admin_.save()
    return admin_

async def delete_admin(id: PydanticObjectId) -> bool:
    admin = await Admin.find_one(Admin.id == id)
    if admin:
        await admin.delete()
        return True
