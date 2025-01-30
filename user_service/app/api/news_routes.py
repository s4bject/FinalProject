from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from service.user_service import post_news, get_news
from service.token_service import role_required
from database.database import get_db
from schemas.schemas import NewsResponse
from typing import List

router = APIRouter()


@router.post("/news", response_model=NewsResponse, dependencies=[Depends(role_required(["super_admin"]))])
async def create_news(text: str, head: str, db: AsyncSession = Depends(get_db)):
    return await post_news(db, head, text)


@router.get("/news", response_model=List[NewsResponse])
async def fetch_news(db: AsyncSession = Depends(get_db)):
    return await get_news(db)
