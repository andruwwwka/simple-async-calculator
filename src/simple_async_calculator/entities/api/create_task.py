from pydantic import BaseModel, Field

from simple_async_calculator.enums.operator import Operator


class CreateTaskRequest(BaseModel):
    """Схема запроса на создание задачи"""

    x: int = Field(title="Левый операнд математического выражения")
    y: int = Field(title="Правый операнд математического выражения")
    operator: Operator = Field(title="Математическая операция")


class CreateTaskResponse(BaseModel):
    """Схема ответа ручки создания задачи"""

    id: int = Field(title="Идентификатор созданной задачи на вычисление")

    class Config:
        orm_mode = True
