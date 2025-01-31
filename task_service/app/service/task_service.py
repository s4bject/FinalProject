from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task, Meet, MeetParticipant


async def get_task(db: AsyncSession, user_id: int):
    result = await db.execute(select(Task).where(Task.worker_id == user_id))
    tasks = result.scalars().all()

    return tasks


async def add_task_for_user(db: AsyncSession, task: str,
                            worker_id: int, task_manager_id: int,
                            date_create: date, deadline: date, ):
    new_task = Task(
        task=task,
        worker_id=worker_id,
        task_manager_id=task_manager_id,
        date_create=date_create,
        deadline=deadline,
        commentary=None,
        grade=None,
    )

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task


async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    current_task = result.scalars().first()
    if not current_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    try:
        await db.delete(current_task)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Невозможно удалить задачу {e}")

    return


async def delete_all_tasks_for_user(db: AsyncSession, user_id: int):
    await db.execute(delete(Task).where(Task.worker_id == user_id))
    await db.commit()

    return


async def update_task(db: AsyncSession, task_id: str, task):
    result = await db.execute(select(Task).where(Task.id == task_id))
    current_task = result.scalars().first()
    if not current_task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    update_data = task.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_task, field, value)

    db.add(current_task)
    await db.commit()
    await db.refresh(current_task)

    return current_task
