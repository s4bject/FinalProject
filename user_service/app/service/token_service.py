from datetime import datetime, timedelta
from typing import List

import jwt
from fastapi import HTTPException, Depends, Request
from database.config import SECRET_KEY

ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_from_cookies(request: Request):
    auth_token = request.cookies.get("auth_token")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Необходима авторизация")
    return auth_token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Не удалось проверить токен")


def role_required(roles: List[str]):
    def role_check(token: str = Depends(get_token_from_cookies)):
        payload = decode_access_token(token)
        if payload.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Недостаточно прав для доступа")
        return payload

    return role_check
