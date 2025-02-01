from fastapi import APIRouter, Depends
from datetime import date
import httpx
import os
from service.token_service import role_required

router = APIRouter()
URL = os.environ.get('TASK_SERVICE')


@router.post("/add_task_for_{user_id}_from_{manag_id}", dependencies=[Depends(role_required(["super_admin", "company_admin"]))])
async def add_task(user_id: int, manag_id: int, task: str, deadline: date):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{URL}/add_task_for_{user_id}_from_{manag_id}",
            json={"task": task, "deadline": str(deadline)}
        )
    return response.json()


@router.get("/task_for_{user_id}")
async def get_tasks(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL}/task_for_{user_id}")
    return response.json()


@router.delete("/delete_task", dependencies=[Depends(role_required(["super_admin", "company_admin"]))])
async def delete_task(task_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{URL}/delete_task", params={"task_id": task_id})
    return response.json()


@router.put("/comment_task", dependencies=[Depends(role_required(["regular", "super_admin"]))])
async def comment_task_user(task_id: int, commentary: str):
    async with httpx.AsyncClient() as client:
        json_data = {
            "commentary": commentary
        }
        response = await client.put(
            f"{URL}/update_task_{task_id}",
            json=json_data
        )
    return response.json()


@router.put("/edit_task", dependencies=[Depends(role_required(["super_admin", "company_admin"]))])
async def grade_task_admin(task_id: int, grade: str, deadline: str, task: str):
    async with httpx.AsyncClient() as client:
        json_data = {
            "task": task,
            "grade": grade,
            "deadline": deadline
        }
        response = await client.put(
            f"{URL}/grade_task_{task_id}",
            json=json_data
        )
    return response.json()
