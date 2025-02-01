from datetime import date
from typing import Annotated, List
from schemas.schemas import TaskResponse, TaskUpdateAdmin, TaskUpdateUser, MeetResponse, MeetUpdateRequest
from fastapi import APIRouter, Depends, Path, Body
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from service.task_service import (add_task_for_user, delete_task,
                                  update_task, get_task,
                                  delete_all_tasks_for_user)
from service.meet_service import (create_meet, get_meets, delete_meet, update_meet)

router = APIRouter()


@router.post("/add_task_for_{user_id}_from_{manag_id}", response_model=TaskResponse)
async def add_task_route(
        user_id: Annotated[int, Path(...)],
        manag_id: Annotated[int, Path(...)],
        task: Annotated[str, Body(...)],
        deadline: Annotated[str, Body(...)],
        db: AsyncSession = Depends(get_db)
):
    deadline_date = date.fromisoformat(deadline)
    try:
        new_user = await add_task_for_user(db, task, user_id, manag_id, date.today(), deadline_date)
        return new_user
    except Exception as e:
        return e


@router.get("/task_for_{user_id}", response_model=List[TaskResponse])
async def get_tasks_route(user_id: Annotated[int, Path(...)],
                          db: AsyncSession = Depends(get_db)):
    try:
        tasks = await get_task(db, user_id)
        return tasks
    except Exception as e:
        return e


@router.delete("/delete_task")
async def delete_task_route(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await delete_task(db, task_id)
        return {"message": "Задача удалена"}
    except Exception as e:
        return e


@router.delete("/delete_task_with_{user_id}")
async def delete_tasks_route(user_id: Annotated[int, Path(...)],
                             db: AsyncSession = Depends(get_db)):
    try:
        await delete_all_tasks_for_user(db, user_id)
        return {"message": "Задача пользователя удалены"}
    except Exception as e:
        return e


@router.put("/update_task_{task_id}", response_model=TaskResponse)
async def update_task_route_user(task: TaskUpdateUser, task_id: Annotated[int, Path(...)],
                                 db: AsyncSession = Depends(get_db)):
    try:
        result = await update_task(db, task_id, task)
        return result
    except Exception as e:
        return e


@router.put("/grade_task_{task_id}", response_model=TaskResponse)
async def update_task_route_admin(task: TaskUpdateAdmin, task_id: Annotated[int, Path(...)],
                                  db: AsyncSession = Depends(get_db)):
    try:
        result = await update_task(db, task_id, task)
        return result
    except Exception as e:
        return e


@router.post("/add_meet_for_{user_id}_from_{manag_id}_name_{name}", response_model=MeetResponse)
async def add_task_route(
        user_id: Annotated[int, Path(...)],
        manag_id: Annotated[int, Path(...)],
        name: Annotated[str, Path(...)],
        db: AsyncSession = Depends(get_db)
):
    try:
        new_user = await create_meet(db, name, user_id, manag_id, date.today())
        return new_user
    except Exception as e:
        return e


@router.get("/meet_for_{user_id}", response_model=List[MeetResponse])
async def get_meets_route(user_id: Annotated[int, Path(...)],
                          db: AsyncSession = Depends(get_db)):
    try:
        tasks = await get_meets(db, user_id)
        return tasks
    except Exception as e:
        return e


@router.delete("/delete_meet")
async def delete_meets_route(meet_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await delete_meet(db, meet_id)
        return {"message": "Встреча удалена"}
    except Exception as e:
        return e


@router.put("/update_meet/{meet_id}", response_model=MeetResponse)
async def update_meet_route(
        meet_id: Annotated[int, Path(...)],
        meet_update: MeetUpdateRequest,
        db: AsyncSession = Depends(get_db)
):
    try:
        updated_meet = await update_meet(db, meet_id, meet_update.name, meet_update.date, meet_update.new_participants)
        return updated_meet
    except Exception as e:
        return e
