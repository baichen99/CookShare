from fastapi import Depends, APIRouter, status
from auth.jwt_handler import decode_jwt
from auth.jwt_bearer import JWTBearer
from models.dish import DishResponse, DishListResponse, DishUpdate
from models.dish import DishQuery, DishCreate
from middlewares.error_handler import JSONException
from services.dish import get_dish_by_id, create_dish, delete_dish, update_dish, get_dishes

from beanie import PydanticObjectId


jwt_bearer = JWTBearer()

router = APIRouter()

@router.get("/{id}", response_model=DishResponse, tags=["Dish"])
async def get_dish(id: PydanticObjectId):
    dish = await get_dish_by_id(id)
    if not dish:
        raise JSONException(404, "Dish not found")
    return dish.dict()

@router.get("/", response_model=DishListResponse, tags=["Dish"])
async def list_dishes(query: DishQuery = Depends()):
    if query.kitchen_id:
        query.kitchen_id = PydanticObjectId(query.kitchen_id)
    dishes = await get_dishes(query)
    return DishListResponse(
        skip=query.skip,
        limit=query.limit,
        total=len(dishes),
        dishes=dishes
    )

@router.post("/", response_model=DishResponse, tags=["Dish"],
            status_code=status.HTTP_201_CREATED)
async def create(form: DishCreate, token: str = Depends(jwt_bearer)):
    payload = decode_jwt(token)
    user_id = payload['user_id']
    form.creator_id = user_id
    # check if kitchen exists
    dishes = await get_dishes(DishQuery(name=form.name, kitchen_id=form.kitchen_id))
    if dishes:
        raise JSONException(400, "Dish already exists")
    dish = await create_dish(form.dict())
    return dish.dict()

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Dish"])
async def update(id: str, form: DishUpdate, token: str = Depends(jwt_bearer)):
    payload = decode_jwt(token)
    user_id = payload['user_id']
    # 验证是否是dish的创建者
    dish = await get_dish_by_id(id)
    if not dish:
        raise JSONException(404, "Dish not found")
    if str(dish.creator_id) != user_id:
        print(dish.creator_id, user_id)
        raise JSONException(403, "You are not the creator of this dish")
    await update_dish(id, form.dict(exclude_unset=True))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Dish"])
async def delete(id: str, token: str = Depends(jwt_bearer)):
    payload = decode_jwt(token)
    user_id = payload['user_id']
    # 验证是否是dish的创建者
    dish = await get_dish_by_id(id)
    if not dish:
        raise JSONException(404, "Dish not found")
    if str(dish.creator_id) != user_id:
        print(dish.creator_id, user_id)
        raise JSONException(403, "You are not the creator of this dish")
    await delete_dish(id)