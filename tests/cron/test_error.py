from datetime import datetime, timezone

import pytest
from sqlalchemy.exc import IntegrityError

from simple_async_calculator.enums.operator import Operator
from simple_async_calculator.enums.status import Status
from simple_async_calculator.services.calculator import UnsupportedOperation
from simple_async_calculator.services.cron import TaskProcessException, process_task
from simple_async_calculator.storage.tables import Task
from simple_async_calculator.storage.task import TaskDAL

TASK_DATA = {
    "id": 1,
    "x": 5,
    "y": 7,
    "operator": Operator.SUMMATION.value,
    "status": Status.PENDING.value,
    "created": datetime.now(timezone.utc),
    "updated": datetime.now(timezone.utc),
}


class DALUpdateMocker:  # pylint: disable=too-few-public-methods
    """Mock функции обнолвения данных в базе"""

    def __init__(self, exception):
        self.exc = exception

    async def __call__(self, task):
        if task.status == Status.ERROR:
            return None
        raise self.exc("test", "test", "test")


@pytest.mark.anyio
@pytest.mark.parametrize(
    "inner_exc,outer_exc",
    [
        (IntegrityError, TaskProcessException),
        (UnsupportedOperation, TaskProcessException),
        (BaseException, BaseException),
    ],
)
async def test_cron__process_task__raises_exception(
    mocker, mock_get_task_dal, inner_exc, outer_exc
):
    """Тест корректного проброса исключения функцией расчета задачи"""
    # arrange
    mocker.patch.object(TaskDAL, "update", DALUpdateMocker(inner_exc))
    task = Task(**TASK_DATA)

    # assert
    with pytest.raises(outer_exc):
        async for dal in mock_get_task_dal():
            await process_task(dal=dal, task=task)
