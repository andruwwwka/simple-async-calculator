import pytest
from fastapi.testclient import TestClient

import simple_async_calculator.storage.task
from simple_async_calculator.api.handlers import app


@pytest.fixture(scope="session")
def client():
    """Фикстура клиента для приложения"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def storage(mocker):
    """Фикстура хранилища.

    Обеспечивает изолирование данных для каждого теста"""
    return mocker.patch.object(
        simple_async_calculator.storage.task, "TASKS_CONTAINER", []
    )
