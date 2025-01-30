from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from service.user_service import update_user_info, delete_user
from service.token_service import role_required
from database.database import get_db
import httpx
import os

router = APIRouter()
URL = os.environ.get('TASK_SERVICE')


@router.post("/update_user/", dependencies=[Depends(role_required(["super_admin", "company_admin"]))])
async def update_user(user_id: int, user_data: dict, db: AsyncSession = Depends(get_db)):
    await update_user_info(db, user_data, user_id)
    return {"message": "Пользователь успешно обновлен"}


@router.delete("/delete_user/", dependencies=[Depends(role_required(["super_admin"]))])
async def delete_user_route(user_id: int, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{URL}/delete_task_with_{user_id}")
    if response.status_code == 200:
        await delete_user(db, user_id)
        return {"message": "Пользователь успешно удален"}
    return {"message": "Ошибка удаления задач пользователя", "data": response.json()}
