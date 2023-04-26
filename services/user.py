from typing import Optional, List
from beanie import Document
from beanie import PydanticObjectId
from beanie.exceptions import DocumentNotFound
from beanie.operators import Eq, RegEx
from pydantic import EmailStr
from models.user import UserQuery


class User(Document):
    username: str
    email: EmailStr
    password: str

    class Settings:
        collection = "user"
        
    def to_dict(self):
        d = {}
        for k, v in self.dict().items():
            # convert ObjectId to str
            if k == 'id':
                d['id'] = str(v)
            else:
                d[k] = v
        return d


async def get_user_by_id(id: PydanticObjectId):
    user = await User.get(id)
    return user

async def get_user_by_email(email: str):
    user = await User.find_one(User.email == email)
    return user

async def get_users(query: UserQuery) -> List[User]:
    query_list = []
    if query.username:
        query_list.append(RegEx(User.username, query.username))
    if query.email:
        query_list.append(Eq(User.email, query.email))
    users = await User.find_many(
        *query_list
    ).skip(query.skip).limit(query.limit).sort(
        (query.sort_by, query.order)
        ).to_list()
    return users

async def create_user(user: User) -> User:
    user_ = await user.create()
    return user_

async def update_user(id: PydanticObjectId, user: User) -> User:
    user_ = await get_user_by_id(id)
    if not user_:
        raise DocumentNotFound
    values = user.dict(exclude_unset=True)
    for key, value in values.items():
        setattr(user_, key, value)
    await user_.save()
    return user_

async def delete_user(id: PydanticObjectId) -> bool:
    user = await User.find_one(User.id == id)
    if user:
        await user.delete()
        return True
