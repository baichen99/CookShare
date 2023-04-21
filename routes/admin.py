from fastapi import FastAPI, Depends, APIRouter
from auth.jwt_handler import sign_jwt
from models.admin import AdminSignIn, AdminResponse
from services.admin import get_admin_by_email
from passlib.context import CryptContext


hash_helper = CryptContext(schemes=["bcrypt"])

router = APIRouter()

@router.post("/login")
async def login(form: AdminSignIn):
    admin = await get_admin_by_email(form.email)
    if not admin:
        return {"message": "Invalid credentials"}
    if not hash_helper.verify(form.password, admin.password):
        return {"message": "Invalid credentials"}
    token = sign_jwt(admin.id, 'admin')
    return AdminResponse(email=admin.email, token=token)