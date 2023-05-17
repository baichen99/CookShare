from beanie import Document
from beanie import PydanticObjectId
from beanie.exceptions import DocumentNotFound
from beanie.operators import Eq, RegEx
from models.user import UserQuery


class User(Document):
    username: str
    email: str
    password: str

    class Settings:
        name = "user"
        
    def to_dict(self):
        d = {}
        for k, v in self.dict().items():
            # convert ObjectId to str
            if type(v) == PydanticObjectId:
                d[k] = str(v)
            else:
                d[k] = v
        return d

async def get_user_by_id(id: PydanticObjectId):
    user = await User.get(id)
    return user

async def get_user_by_email(email: str):
    user = await User.find_one(User.email == email)
    return user

async def get_users(query: UserQuery) -> list[User]:
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

async def create_user(values: dict) -> User:
    user = User(**values)
    user_ = await user.create()
    return user_

async def update_user(id: PydanticObjectId, values: dict):
    user_ = await get_user_by_id(id)
    if not user_:
        raise DocumentNotFound
    for key, value in values.items():
        setattr(user_, key, value)
    await user_.save()

async def delete_user(id: PydanticObjectId):
    user = await User.find_one(User.id == id)
    if user:
        await user.delete()

