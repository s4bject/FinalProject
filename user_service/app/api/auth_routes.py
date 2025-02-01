from fastapi import APIRouter, Depends, Response
from pydantic import EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from service.auth_service import authenticate_user, user_registration
from service.token_service import create_access_token
from database.database import get_db
from schemas.schemas import UserResponse
from typing import Annotated

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
        email: Annotated[EmailStr, Field(max_length=255)],
        full_name: Annotated[str, Field(max_length=255)],
        password: Annotated[str, Field(min_length=4, max_length=255)],
        invite_code: Annotated[str, Field(max_length=8)] = None,
        db: AsyncSession = Depends(get_db)
):
    return await user_registration(db, email, full_name, password, invite_code)


@router.post("/login")
async def login_user(
        email: Annotated[EmailStr, Field(max_length=255)],
        password: Annotated[str, Field(min_length=4, max_length=255)],
        response: Response,
        db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, email, password)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    response.set_cookie(key="auth_token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}
