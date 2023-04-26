from fastapi import Depends, APIRouter
from auth.jwt_handler import sign_jwt, decode_jwt, TokenResponse
from auth.jwt_bearer import JWTBearer
from models.user import UserLogin, UserRegister, UserUpdate, UserQuery
from models.user import UserResponse, UserListResponse
from services.user import get_user_by_email, get_user_by_id, get_users, create_user, update_user
from services.user import User
from middlewares.error_handler import JSONException
from passlib.context import CryptContext


jwt_bearer = JWTBearer()

hash_helper = CryptContext(schemes=["bcrypt"])

router = APIRouter()

@router.post("/login", tags=["User"], description="User login", response_model=TokenResponse)
async def login(form: UserLogin):
    user = await get_user_by_email(form.email)
    if (not user) or (not hash_helper.verify(form.password, user.password)):
        raise JSONException(status_code=401, error_msg="Invalid credentials")
    token_rsp = sign_jwt(str(user.id), role='user')
    return token_rsp

@router.post("/register", tags=["User"], description="User register", response_model=UserResponse)
async def register(form: UserRegister):
    user = await get_user_by_email(form.email)
    if user:
        raise JSONException(status_code=400, error_msg="Email already exists")
    hashed_password = hash_helper.hash(form.password)
    user = User(username=form.username, email=form.email, password=hashed_password)
    user = await create_user(user)
    return user

@router.get("/", tags=["User"], description="Get all users")
async def list_users(query: UserQuery = Depends(), token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    if decoded_token['role'] != 'admin':
        raise JSONException(status_code=401, error_msg="Unauthorized")
    users = await get_users(query)

    users = [user.to_dict() for user in users]
    return UserListResponse(
        skip=query.skip,
        limit=query.limit,
        total=len(users),
        users=users
    )
    
@router.get('/{id}', tags=['User'], description='Get user', response_model=UserResponse)
async def get_user(id: str):
    user = await get_user_by_id(id)
    return user.to_dict()

@router.put("/{id}", tags=["User"], description="Update user", response_model=UserResponse)
async def update(id: str, form: UserUpdate, token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    user_id = decoded_token['user_id']
    if decoded_token['role'] != 'admin' and id != user_id:
        raise JSONException(status_code=401, error_msg="Unauthorized")
    user = await get_user_by_email(form.email)
    if user and str(user.id) != id:
        raise JSONException(status_code=400, error_msg="Email already exists")
    user = await update_user(id, form)
    return user.to_dict()
