from pydantic import BaseModel

from simple_async_calculator.enums.status import Status


class TaskItem(BaseModel):
    """Вложенный элемент задачи в списке доступных"""

    id: int
    status: Status


class TaskListingResponse(BaseModel):
    """Схема ответа ручки листинга задач"""

    tasks: list[TaskItem]
