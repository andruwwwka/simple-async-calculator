from pydantic import BaseModel, Field

from simple_async_calculator.enums.status import Status


class TaskItem(BaseModel):
    """Вложенный элемент задачи в списке доступных"""

    id: int = Field(title="Идентификатор задачи")
    status: Status = Field(title="Статус выполнения задачи")

    class Config:  # pylint: disable=too-few-public-methods,missing-class-docstring
        orm_mode = True


class TaskListingResponse(BaseModel):
    """Схема ответа ручки листинга задач"""

    tasks: list[TaskItem] = Field(title="Список всех задач")
