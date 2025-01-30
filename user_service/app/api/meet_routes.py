from fastapi import APIRouter, Depends
import httpx
import os
from service.token_service import role_required
from schemas.schemas import ExternalMeetUpdateRequest

router = APIRouter()
URL = os.environ.get('TASK_SERVICE')


@router.post("/add_meet_for_{user_id}_from_{manag_id}",
             dependencies=[Depends(role_required(["super_admin", "company_admin"]))])
async def add_meet(user_id: int, manag_id: int, name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{URL}/add_meet_for_{user_id}_from_{manag_id}_name_{name}")
    return response.json()


@router.get("/meet_for_{user_id}")
async def get_meets(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{URL}/meet_for_{user_id}")
    return response.json()


@router.delete("/delete_meet", dependencies=[Depends(role_required(["super_admin", "company_admin"]))])
async def delete_meet(meet_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{URL}/delete_meet", params={"meet_id": meet_id})
    return response.json()


@router.post("/external_update_meet")
async def external_update_meet(meet_data: ExternalMeetUpdateRequest):
    url = f"{URL}/update_meet/{meet_data.meet_id}"
    json_data = meet_data.model_dump()

    async with httpx.AsyncClient() as client:
        response = await client.put(url, json=json_data)
        return response.json()
