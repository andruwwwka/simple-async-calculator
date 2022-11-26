from pydantic import BaseModel, Field

from simple_async_calculator.enums.status import Status


class TaskDetailResponse(BaseModel):
    """Схема ответа для ручки получения результата задачи"""

    status: Status = Field(title="Статус выполнения задачи")
    result: float | None = Field(
        title="Результат выполнения математической операции",
        default=None,
    )

    class Config:
        orm_mode = True
