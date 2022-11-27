import pytest

from simple_async_calculator.enums.operator import Operator
from simple_async_calculator.enums.status import Status


@pytest.mark.anyio
async def test_create_task(client):
    """Тест метода API создания задачи"""
    # act
    response = await client.post(
        "/tasks",
        json={
            "x": 1,
            "y": 2,
            "operator": Operator.SUMMATION.value,
        },
    )

    # assert
    assert response.status_code == 201
    assert response.json() == {"id": 1}


@pytest.mark.anyio
async def test_tasks_listing__empty(client):
    """Тест получения пустого списка задач через API"""
    # act
    response = await client.get("/tasks")

    # assert
    assert response.status_code == 200
    assert response.json() == {"tasks": []}


@pytest.mark.anyio
async def test_tasks_listing__with_task_items(client):
    """Тест получения списка задач через API"""
    # arrange
    create_response = await client.post(
        "/tasks",
        json={
            "x": 1,
            "y": 2,
            "operator": Operator.SUMMATION.value,
        },
    )
    existing_task_id = create_response.json()["id"]

    # act
    response = await client.get("/tasks")

    # assert
    assert response.status_code == 200
    assert response.json() == {
        "tasks": [
            {
                "id": existing_task_id,
                "status": Status.PENDING.value,
            },
        ],
    }


@pytest.mark.anyio
async def test_task_detail(client):
    """Тест метода API для получения резултьтатов вычислений"""
    # arrange
    create_response = await client.post(
        "/tasks",
        json={
            "x": 8,
            "y": 2,
            "operator": Operator.SUMMATION.value,
        },
    )
    existing_task_id = create_response.json()["id"]

    # act
    response = await client.get(f"/tasks/{existing_task_id}")

    # assert
    assert response.status_code == 200
    assert response.json() == {
        "status": Status.PENDING.value,
        "result": None,
    }
