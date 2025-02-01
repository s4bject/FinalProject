import pytest
from fastapi.testclient import TestClient
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.main import app

print(sys.path)
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_client(client):
    res = client.post("/login?email=j%40j.com&password=1234")
    assert res.status_code == 200
    token = res.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


def test_client(client):
    res = client.get("/news")
    assert res.status_code == 200


def test_task(client):
    res = client.get("/task_for_10")
    assert res.status_code == 200


def test_login(client):
    res = client.post("/login?email=j%40j.com&password=1234")
    assert res.status_code == 200


def test_login_incorrect(client):
    res = client.post("/login?email=j%40j.com&password=12346")
    assert res.status_code == 400


def test_register_missing_params(client):
    res = client.post("/register?email=test%40test.com&password=1234")
    assert res.status_code == 422


def test_get_meets(client):
    res = client.get("/meet_for_1")
    assert res.status_code == 200


def test_delete_meet(auth_client):
    res = auth_client.delete("/delete_meet?meet_id=1")
    assert res.status_code in [200, 403]


def test_create_news(auth_client):
    res = auth_client.post("/news?text=Some%20news&head=Headline")
    assert res.status_code in [200, 403]


def test_fetch_news(client):
    res = client.get("/news")
    assert res.status_code == 200


def test_add_task(auth_client):
    res = auth_client.post("/add_task_for_1_from_2?task=Complete%20Project&deadline=2025-12-31")
    assert res.status_code in [200, 403]


def test_get_tasks(auth_client):
    res = auth_client.get("/task_for_1")
    assert res.status_code == 200


def test_delete_task(auth_client):
    res = auth_client.delete("/delete_task?task_id=1")
    assert res.status_code in [200, 403]


def test_edit_task(auth_client):
    res = auth_client.put("/edit_task?task_id=1&grade=A&deadline=2025-12-31&task=Updated%20Task")
    assert res.status_code in [200, 403]
