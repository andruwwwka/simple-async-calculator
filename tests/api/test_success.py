import pytest


def test_create_task(client):
    """Тест метода API создания задачи"""
    # act
    response = client.post(
        "/tasks",
        json={
            "x": 1,
            "y": 2,
            "operator": "+",
        },
    )

    # assert
    assert response.status_code == 201
    assert response.json() == {"id": 1}


def test_tasks_listing__empty(client):
    """Тест получения пустого списка задач через API"""
    # act
    response = client.get("/tasks")

    # assert
    assert response.status_code == 200
    assert response.json() == {"tasks": []}


def test_tasks_listing__with_task_items(client):
    """Тест получения списка задач через API"""
    # arrange
    create_response = client.post(
        "/tasks",
        json={
            "x": 1,
            "y": 2,
            "operator": "+",
        },
    )
    existing_task_id = create_response.json()["id"]

    # act
    response = client.get("/tasks")

    # assert
    assert response.status_code == 200
    assert response.json() == {
        "tasks": [
            {
                "id": existing_task_id,
                "status": "pending",
            },
        ],
    }


@pytest.mark.parametrize(
    "operator,result",
    [
        ("+", 10),
        ("-", 6),
        ("*", 16),
        ("/", 4),
    ],
)
def test_task_detail(client, operator, result):
    """Тест метода API для получения резултьтатов вычислений"""
    # arrange
    create_response = client.post(
        "/tasks",
        json={
            "x": 8,
            "y": 2,
            "operator": operator,
        },
    )
    existing_task_id = create_response.json()["id"]

    # act
    response = client.get(f"/tasks/{existing_task_id}")

    # assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "result": result,
    }
