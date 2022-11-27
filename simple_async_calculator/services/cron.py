import asyncio
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from simple_async_calculator.entities.db import UpdateTaskDB
from simple_async_calculator.enums.status import Status
from simple_async_calculator.services.calculator import UnsupportedOperation, calculate
from simple_async_calculator.storage.dependencies import get_task_dal
from simple_async_calculator.storage.tables import Task
from simple_async_calculator.storage.task import TaskDAL


class TaskProcessException(Exception):
    """Исключение для неподдерживаемой операции"""


async def process_task(*, dal: TaskDAL, task: Task):
    """Логика обработчика отельно взятой задачи"""
    updated = datetime.now(timezone.utc)
    try:
        result = calculate(x=task.x, y=task.y, operator=task.operator)
        await dal.update(
            UpdateTaskDB(
                id=task.id,
                result=result,
                updated=updated,
                status=Status.SUCCESS,
            )
        )
    except (IntegrityError, UnsupportedOperation) as exc:
        await dal.update(
            UpdateTaskDB(
                id=task.id,
                status=Status.ERROR,
                updated=updated,
            )
        )
        raise TaskProcessException from exc
    except BaseException as exc:
        raise exc


async def cron_service():
    """Логика работы крона по расчету результатов задач"""
    async for dal in get_task_dal():
        tasks = await dal.get_all(status=Status.PENDING)
        await asyncio.gather(
            *[process_task(dal=dal, task=task) for task in tasks],
            return_exceptions=True,
        )
