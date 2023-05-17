from fastapi import Depends, APIRouter, status
from auth.jwt_handler import decode_jwt
from auth.jwt_bearer import JWTBearer
from models.kitchen import KitchenResponse, KitchenListResponse
from models.kitchen import KitchenQuery, KitchenCreate, KitchenUpdate
from middlewares.error_handler import JSONException
from services.kitchen import Kitchen
from services.kitchen import get_kitchen_by_id, get_kitchens, create_kitchen, delete_kitchen, update_kitchen

from beanie import PydanticObjectId


jwt_bearer = JWTBearer()

router = APIRouter()

@router.get('/{id}', description='Get kitchen by id', response_model=KitchenResponse)
async def get_kitchen(id: str):
    kitchen = await get_kitchen_by_id(id)
    if kitchen is None:
        raise JSONException(404, 'Kitchen not found')
    return kitchen.dict()

@router.get('/', description='Get all kitchens', response_model=KitchenListResponse)
async def list_kitchens(query: KitchenQuery = Depends(), token: str = Depends(jwt_bearer)):
    if query.owner_id:
        query.owner_id = PydanticObjectId(query.owner_id)
    kitchens = await get_kitchens(query)
    return KitchenListResponse(
        skip=query.skip,
        limit=query.limit,
        total=len(kitchens),
        kitchens=kitchens
    )

@router.post('/', description='Create new kitchen', response_model=KitchenResponse,
             status_code=status.HTTP_201_CREATED)
async def create(form: KitchenCreate, token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    user_id = decoded_token['user_id']
    # 同一用户最多创建3个厨房
    # 同一用户下的厨房名称不能重复
    my_kitchens = await get_kitchens(KitchenQuery(owner_id=user_id))
    if len(my_kitchens) >= 3:
        raise JSONException(400, 'You can only create 3 kitchens')
    if any(kitchen.name == form.name for kitchen in my_kitchens):
        raise JSONException(400, 'Kitchen name already exists')
    form_data = form.dict()
    form_data['owner_id'] = PydanticObjectId(user_id)
    kitchen = await create_kitchen(form_data)
    return kitchen.dict()

@router.put('/{id}', description='Update kitchen by id',
            status_code=status.HTTP_204_NO_CONTENT)
async def update(id: str, form: KitchenUpdate, token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    user_id = decoded_token['user_id']
    kitchen = await get_kitchen_by_id(id)
    if kitchen is None:
        raise JSONException(404, 'Kitchen not found')
    if str(kitchen.owner_id) != user_id:
        print(f"owner_id: {kitchen.owner_id}, user_id: {user_id}")
        raise JSONException(403, 'You are not the owner of this kitchen')
    await update_kitchen(kitchen.id, form.dict(exclude_unset=True))

@router.delete('/{id}', description='Delete kitchen by id',
               status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    user_id = decoded_token['user_id']
    kitchen = await get_kitchen_by_id(id)
    if kitchen is None:
        raise JSONException(404, 'Kitchen not found')
    if str(kitchen.owner_id) != user_id:
        raise JSONException(403, 'You are not the owner of this kitchen')
    await delete_kitchen(id)
