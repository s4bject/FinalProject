from datetime import date
import pytest
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from service.task_service import add_task_for_user, get_task, delete_task, delete_all_tasks_for_user, \
    update_task
from schemas.schemas import TaskUpdateAdmin
from database.models import Task


@pytest.mark.asyncio
async def test_add_task_for_user(mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    result = await add_task_for_user(
        mock_session, "Test Task", 1, 2, date.today(), date.today()
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    assert isinstance(result, Task)
    assert result.task == "Test Task"


@pytest.mark.asyncio
async def test_get_task(mock_session):
    mock_task = Task(
        id=1,
        task="Test Task",
        worker_id=1,
        task_manager_id=2,
        deadline=date.today(),
        date_create=date.today()
    )
    mock_session.execute.return_value.scalars.return_value.all.return_value = [mock_task]

    tasks = await get_task(mock_session, 1)

    mock_session.execute.assert_awaited_once()
    assert len(tasks) == 1
    assert tasks[0].task == "Test Task"


@pytest.mark.asyncio
async def test_delete_task(mock_session):
    mock_session.execute.return_value = MagicMock(rowcount=1)

    await delete_task(mock_session, 1)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_all_tasks_for_user(mock_session):
    mock_session.execute.return_value = MagicMock(rowcount=2)

    await delete_all_tasks_for_user(mock_session, 1)

    mock_session.execute.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_task(mock_session):
    mock_task = Task(
        id=1,
        task="Old Task",
        worker_id=1,
        task_manager_id=2,
        deadline=date.today(),
        date_create=date.today()
    )
    mock_session.execute.return_value.scalars.return_value.first.return_value = mock_task

    update_data = TaskUpdateAdmin(task="Updated Task", deadline=date.today())
    updated_task = await update_task(mock_session, 1, update_data)

    mock_session.execute.assert_awaited()
    mock_session.commit.assert_awaited_once()
    assert updated_task.task == "Updated Task"