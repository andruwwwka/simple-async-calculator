from simple_async_calculator.entities.db.task import BaseTaskDB, TaskDB
from simple_async_calculator.enums.status import Status

TASKS_CONTAINER: list[TaskDB] = []


class TaskDoesNotExists(Exception):
    """Исключение при невозможности получить задачу"""


def create_task(task: BaseTaskDB) -> int:
    """Создание задачи в хранилище"""
    task_id = len(TASKS_CONTAINER) + 1
    TASKS_CONTAINER.append(
        TaskDB(
            id=task_id,
            **task.dict(),
        )
    )
    return task_id


def get_tasks() -> list[TaskDB]:
    """Получение всех задач из хранилища"""
    return TASKS_CONTAINER


def get_task_by_id(task_id: int) -> TaskDB:
    """Получение из хранилища конкретной задачи"""
    try:
        return next(filter(lambda tsk: tsk.id == task_id, TASKS_CONTAINER))
    except StopIteration as exc:
        raise TaskDoesNotExists from exc


def update_task(*, task_id: int, result: float, status: Status) -> TaskDB:
    """Обновление задачи в хранилище"""
    task = get_task_by_id(task_id)
    task.result = result
    task.status = status
    TASKS_CONTAINER[task_id - 1] = task
    return task
