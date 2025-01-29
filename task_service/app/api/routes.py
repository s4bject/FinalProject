from datetime import date
from typing import Annotated, List
from schemas.schemas import TaskResponse, TaskUpdateAdmin, TaskUpdateUser, MeetResponse
from fastapi import APIRouter, Depends, Path
from pydantic import Field
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from service.task_service import (add_task_for_user, delete_task,
                                  update_task, get_task,
                                  delete_all_tasks_for_user)
from service.meet_service import (create_meet, get_meets, delete_meet)

router = APIRouter()


@router.post("/add_task_for_{user_id}_from_{manag_id}", response_model=TaskResponse)
async def add_task_route(
        user_id: Annotated[int, Path(...)],
        manag_id: Annotated[int, Path(...)],
        task: Annotated[str, Field(...)],
        deadline: Annotated[date, Field(...)],
        db: AsyncSession = Depends(get_db)
):
    new_user = await add_task_for_user(db, task, user_id, manag_id, date.today(), deadline)
    return new_user


@router.get("/task_for_{user_id}", response_model=List[TaskResponse])
async def get_tasks_route(user_id: Annotated[int, Path(...)],
                          db: AsyncSession = Depends(get_db)):
    tasks = await get_task(db, user_id)
    return tasks


@router.delete("/delete_task")
async def delete_task_route(task_id: int, db: AsyncSession = Depends(get_db)):
    await delete_task(db, task_id)
    return {"message": "Задача удалена"}


@router.delete("/delete_task_with_{user_id}")
async def delete_tasks_route(user_id: Annotated[int, Path(...)],
                             db: AsyncSession = Depends(get_db)):
    tasks = await delete_all_tasks_for_user(db, user_id)
    return {"message": "Задача пользователя удалены"}


@router.put("/update_task", response_model=TaskResponse)
async def update_task_route_user(task: TaskUpdateUser, task_id: Annotated[int, Field(...)],
                                 db: AsyncSession = Depends(get_db)):
    result = await update_task(db, task_id, task)
    return result


@router.put("/grade_task", response_model=TaskResponse)
async def update_task_route_admin(task: TaskUpdateAdmin, task_id: Annotated[int, Field(...)],
                                  db: AsyncSession = Depends(get_db)):
    result = await update_task(db, task_id, task)
    return result


@router.post("/add_meet_for_{user_id}_from_{manag_id}", response_model=MeetResponse)
async def add_task_route(
        user_id: Annotated[int, Path(...)],
        manag_id: Annotated[int, Path(...)],
        name: Annotated[str, Field(...)],
        db: AsyncSession = Depends(get_db)
):
    new_user = await create_meet(db, name, user_id, manag_id, date.today())
    return new_user


@router.get("/meet_for_{user_id}", response_model=List[MeetResponse])
async def get_meets_route(user_id: Annotated[int, Path(...)],
                          db: AsyncSession = Depends(get_db)):
    tasks = await get_meets(db, user_id)
    return tasks


@router.delete("/delete_meet")
async def delete_meets_route(meet_id: int, db: AsyncSession = Depends(get_db)):
    await delete_meet(db, meet_id)
    return {"message": "Встреча удалена"}
