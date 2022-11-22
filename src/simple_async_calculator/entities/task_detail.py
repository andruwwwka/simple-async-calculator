from pydantic import BaseModel

from simple_async_calculator.enums.status import Status


class TaskDetailResponse(BaseModel):
    """Схема ответа для ручки получения результата задачи"""
    status: Status
    result: float | None = None
