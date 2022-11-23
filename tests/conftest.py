import pytest
from fastapi.testclient import TestClient

from simple_async_calculator.api.handlers import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def storage(mocker):
    import simple_async_calculator.storage.task

    return mocker.patch.object(
        simple_async_calculator.storage.task, "TASKS_CONTAINER", []
    )
