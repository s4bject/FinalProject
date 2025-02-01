from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Company, Department, News
from schemas.schemas import UserUpdate


async def update_user_info(db: AsyncSession, user: UserUpdate, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    current_user = result.scalars().first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    update_data = user.dict(exclude_unset=True)
    for field in ["company_id", "manager_id", "department_id"]:
        if field in update_data and update_data[field] == 0:
            update_data[field] = None
    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user


async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    current_user = result.scalars().first()
    if not current_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    try:
        await db.delete(current_user)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Невозможно удалить пользователя из-за связанных данных {e}")

    return


async def get_news(db: AsyncSession):
    query = select(News)
    result = await db.execute(query)
    news_items = result.scalars().all()
    return news_items


async def post_news(db: AsyncSession, head: str, text: str):
    curr_date = date.today()
    new_news = News(
        head=head,
        description=text,
        date_create=curr_date
    )
    db.add(new_news)
    await db.commit()
    await db.refresh(new_news)

    return new_news
