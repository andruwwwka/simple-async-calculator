import asyncio
import logging
from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from simple_async_calculator.entities.db import UpdateTaskDB
from simple_async_calculator.enums.status import Status
from simple_async_calculator.services.calculator import UnsupportedOperation, calculate
from simple_async_calculator.storage.dependencies import get_task_dal
from simple_async_calculator.storage.tables import Task
from simple_async_calculator.storage.task import TaskDAL

cron_logger = logging.getLogger("cron")


class TaskProcessException(Exception):
    """Исключение для неподдерживаемой операции"""


async def process_task(*, dal: TaskDAL, task: Task):
    """Логика обработчика отельно взятой задачи"""
    cron_logger.debug("Start processing for tasks: id=%s", task.id)
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
        cron_logger.debug("Calculate Task(id=%s) succeed with result %s", task.id, result)
    except (IntegrityError, UnsupportedOperation) as exc:
        await dal.update(
            UpdateTaskDB(
                id=task.id,
                status=Status.ERROR,
                updated=updated,
            )
        )
        cron_logger.warning("Error while calculing Task(id=%s)", task.id)
        raise TaskProcessException from exc
    except BaseException as exc:
        logging.exception("Unrecognized error while processing Task(id=%s)", task.id)
        raise exc


async def cron_service():
    """Логика работы крона по расчету результатов задач"""
    async for dal in get_task_dal():
        tasks = await dal.get_all(status=Status.PENDING)
        cron_logger.debug("Start processing for tasks barch: %s", [t.id for t in tasks])
        await asyncio.gather(
            *[process_task(dal=dal, task=task) for task in tasks],
            return_exceptions=True,
        )
