from fastapi import Depends, APIRouter, status
from auth.jwt_handler import decode_jwt
from auth.jwt_bearer import JWTBearer
from models.order import OrderResponse, OrderListResponse
from models.order import OrderCreate, OrderUpdate
from middlewares.error_handler import JSONException
from services.dish import get_dish_by_id
from services.order import get_order_by_id, create_order, update_order
from beanie import PydanticObjectId


jwt_bearer = JWTBearer()

router = APIRouter()

@router.get('/{id}', description='Get order by id', response_model=OrderResponse)
async def get_order(id: str):
    order = await get_order_by_id(id)
    if order is None:
        raise JSONException(404, 'Order not found')
    return order.dict()

# @router.get('/', description='Get all orders', response_model=OrderListResponse)
# async def list_orders(query: OrderQuery = Depends(), token: str = Depends(jwt_bearer)):
#     orders = await get_orders(query)
#     orders = [order.dict() for order in orders]
#     return OrderListResponse(
#         skip=query.skip,
#         limit=query.limit,
#         total=len(orders),
#         orders=orders
    # )

@router.post('/', description='Create new order')
async def create(form: OrderCreate, token: str = Depends(jwt_bearer), response_model=OrderResponse):
    decoded_token = decode_jwt(token)
    user_id = decoded_token['user_id']
    dishes_id = form.dishes_id
    # 计算所有dish价格
    dish_price = {}
    for dish_id in dishes_id:
        dish = await get_dish_by_id(dish_id)
        dish_price[dish_id] = dish.price
    total_price = sum(dish_price.values())
    form_data = form.dict()
    form_data['total_price'] = total_price
    form_data['customer_id'] = PydanticObjectId(user_id)
    order = await create_order(form_data)
    return order.dict()

@router.put('/{id}', description='Update order by id', status_code=status.HTTP_204_NO_CONTENT)
async def update(id: str, form: OrderUpdate, token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    user_id = decoded_token['user_id']
    order = await get_order_by_id(id)
    if order is None:
        raise JSONException(404, 'Order not found')
    if order.owner_id != user_id:
        raise JSONException(403, 'You are not the owner of this order')
    order = await update_order(order, form)
