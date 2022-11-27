from datetime import datetime, timezone

import pytest

import simple_async_calculator.storage.dependencies
from simple_async_calculator.entities.db import BaseTaskDB
from simple_async_calculator.enums.operator import Operator
from simple_async_calculator.enums.status import Status
from simple_async_calculator.services.cron import cron_service


@pytest.mark.anyio
async def test_cron(mocker, mock_get_task_dal):
    """Тест сервиса крона расчета результатов"""
    # arrage
    mocker.patch.object(
        simple_async_calculator.storage.dependencies, "get_task_dal", mock_get_task_dal
    )
    async for dal in mock_get_task_dal():
        now = datetime.now(timezone.utc)
        task = await dal.create(
            BaseTaskDB(
                x=3,
                y=4,
                operator=Operator.SUMMATION,
                status=Status.PENDING,
                created=now,
                updated=now,
            )
        )

    # act
    await cron_service()
    async for dal in mock_get_task_dal():
        updated_task = await dal.get_one(task.id)

    # assert
    assert task.status == Status.PENDING
    assert task.result is None
    assert task.id == updated_task.id
    assert updated_task.status == Status.SUCCESS
    assert updated_task.result is not None
