def test_task_detail(client):
    """Тест запроса результата несуществующей задачи"""
    # act
    response = client.get("/tasks/1")

    # assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_task_detail__invalid_id(client):
    """Тест обработки некорректного id задачи в ручке результата задачи"""
    # act
    response = client.get("/tasks/0")

    # assert
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"limit_value": 1},
                "loc": ["path", "task_id"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
            }
        ]
    }


def test_create_task__invalid_operator(client):
    """Обработки неподдерживаемого оператора в ручке создания задачи"""
    # act
    response = client.post(
        "/tasks",
        json={
            "x": 454,
            "y": 26,
            "operator": "//",
        },
    )

    # assert
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "ctx": {"enum_values": ["+", "-", "*", "/"]},
                "loc": ["body", "operator"],
                "msg": "value is not a valid enumeration member; permitted: '+', "
                "'-', '*', '/'",
                "type": "type_error.enum",
            }
        ]
    }
