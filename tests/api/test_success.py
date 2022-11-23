def test_create_tasks(client):
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
    # act
    response = client.get("/tasks")

    # assert
    assert response.status_code == 200
    assert response.json() == {"tasks": []}


def test_tasks_listing__with_task_items(client):
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


def test_task_detail(client):
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
    response = client.get(f"/tasks/{existing_task_id}")

    # assert
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "result": 3,
    }
