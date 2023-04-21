from fastapi import Depends, APIRouter
from fastapi.exceptions import HTTPException
from auth.jwt_handler import sign_jwt, decode_jwt
from auth.jwt_bearer import JWTBearer
from models.admin import AdminSignIn
from services.admin import get_admin_by_email, get_admins
from middlewares.error_handler import JSONException
from passlib.context import CryptContext


jwt_bearer = JWTBearer()

hash_helper = CryptContext(schemes=["bcrypt"])

router = APIRouter()

@router.post("/login", tags=["Admin"], description="Admin login")
async def login(form: AdminSignIn):
    admin = await get_admin_by_email(form.email)
    if (not admin) or (not hash_helper.verify(form.password, admin.password)):
        raise JSONException(status_code=401, error_msg="Invalid credentials")
    token_rsp = sign_jwt(str(admin.id), 'admin')
    return token_rsp

@router.get("/", tags=["Admin"], description="Get all admins")
async def list_admins(token: str = Depends(jwt_bearer)):
    decoded_token = decode_jwt(token)
    if decoded_token['role'] != 'admin':
        raise JSONException(status_code=401, error_msg="Unauthorized")
    admins = await get_admins()
    return admins