from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from middlewares.error_handler import JSONException

from .jwt_handler import decode_jwt


def verify_jwt(jwtoken: str) -> bool:
    isTokenValid: bool = False

    payload = decode_jwt(jwtoken)
    if payload:
        isTokenValid = True
    return isTokenValid


class JWTBearer(HTTPBearer):
    # 依赖注入，从请求头中获取token
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise JSONException(status_code=403, error_msg="Invalid authentication token")

            if not verify_jwt(credentials.credentials):
                raise JSONException(status_code=403, error_msg="Invalid token or expired token")

            return credentials.credentials
        else:
            raise JSONException(status_code=403, error_msg="Invalid authorization token")