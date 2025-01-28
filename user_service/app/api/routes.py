from typing import Annotated

from fastapi import APIRouter, Depends, Response
from pydantic import EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from database.database import get_db
from service.user_service import update_user_info, delete_user
from service.auth_service import authenticate_user, user_registration
from service.token_service import create_access_token, get_token_from_cookies, role_required
from schemas.schemas import UserResponse, UserUpdate

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(
        email: Annotated[EmailStr, Field(max_length=255)],
        full_name: Annotated[str, Field(max_length=255)],
        password: Annotated[str, Field(min_length=4, max_length=255)],
        invite_code: Annotated[str, Field(max_length=8)] = None,
        db: AsyncSession = Depends(get_db)
):
    new_user = await user_registration(db, email, full_name, password, invite_code)
    return new_user


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


@router.get("/admin", dependencies=[Depends(role_required("super_admin"))])
async def admin_dashboard():
    return RedirectResponse(url="/admin_ui")


@router.post("/update_user/{id}", dependencies=[Depends(role_required("super_admin"))])
async def update_user(
        user: UserUpdate,
        user_id: int,
        db: AsyncSession = Depends(get_db),
):
    await update_user_info(db, user, user_id)
    return {"message": "Пользователь успешно обновлен"}


@router.delete("/delete_user/{id}", dependencies=[Depends(role_required("super_admin"))])
async def delete_user(
        user_id: int,
        db: AsyncSession = Depends(get_db),
):
    await delete_user(db, user_id)
    return {"message": "Пользователь успешно обновлен"}
