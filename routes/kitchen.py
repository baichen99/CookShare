from fastapi import Depends, APIRouter
from auth.jwt_handler import decode_jwt
from auth.jwt_bearer import JWTBearer
from models.kitchen import KitchenResponse, KitchenListResponse
from models.kitchen import KitchenQuery, KitchenCreate
from middlewares.error_handler import JSONException
from services.kitchen import Kitchen
from services.kitchen import get_kitchen_by_id, get_kitchens, create_kitchen

from beanie import PydanticObjectId


jwt_bearer = JWTBearer()

router = APIRouter()

@router.get('/{id}', description='Get kitchen by id', response_model=KitchenResponse)
async def get_kitchen(id: str):
    kitchen = await get_kitchen_by_id(id)
    if kitchen is None:
        raise JSONException(404, 'Kitchen not found')
    return kitchen.to_dict()

@router.get('/', description='Get all kitchens', response_model=KitchenListResponse)
async def list_kitchens(query: KitchenQuery = Depends(), token: str = Depends(jwt_bearer)):
    kitchens = await get_kitchens(query)
    kitchens = [kitchen.to_dict() for kitchen in kitchens]
    return KitchenListResponse(
        skip=query.skip,
        limit=query.limit,
        total=len(kitchens),
        kitchens=kitchens
    )

@router.post('/', description='Create new kitchen', response_model=KitchenResponse)
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
    kitchen = Kitchen(name=form.name, description=form.description,
                      address=form.address, facilities=form.facilities,
                      owner_id=PydanticObjectId(user_id))
    kitchen = await create_kitchen(kitchen)
    return kitchen.to_dict()

