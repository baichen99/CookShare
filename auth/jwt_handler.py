import time
from typing import Dict
from pydantic import BaseModel
import jwt

from config.config import Settings


class TokenResponse(BaseModel):
    access_token: str
    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjQ0MjJhMzk3MmVlNmUwZTFlOTAwYzY1Iiwicm9sZSI6ImFkbWluIiwiZXhwaXJlcyI6MTY4MjQ3NzQyNi4wOTI5OTR9.LhBHqhnQpNX6wgF4X3CUZE192tGBfTDm--yuit3PDc4"
            }
        }


secret_key = Settings().secret_key


def sign_jwt(user_id: str, role: str='user') -> Dict[str, str]:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'role': role,
        'expires': time.time() + 2400
    }
    return TokenResponse(access_token=jwt.encode(payload, secret_key, algorithm="HS256"))


def decode_jwt(token: str) -> dict:
    # Decode the JWT to get payload
    decoded_token = jwt.decode(token.encode(), secret_key, algorithms=["HS256"])
    return decoded_token if decoded_token['expires'] >= time.time() else {}