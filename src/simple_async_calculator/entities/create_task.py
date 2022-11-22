from pydantic import BaseModel

from simple_async_calculator.enums.operator import Operator


class CreateTaskRequest(BaseModel):
    """Схема запроса на создание задачи"""
    x: int
    y: int
    operator: Operator


class CreateTaskResponse(BaseModel):
    """Схема ответа ручки создания задачи"""
    task_id: int
