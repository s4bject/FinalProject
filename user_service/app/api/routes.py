from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr, Field
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from service.user_service import user_registration
from schemas.schemas import UserResponse

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
