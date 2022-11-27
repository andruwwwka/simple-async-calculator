from datetime import datetime

from pydantic import BaseModel

from simple_async_calculator.enums.operator import Operator
from simple_async_calculator.enums.status import Status


class BaseTaskDB(BaseModel):
    """Объект задачи для создания сущности в хранилище"""

    x: int
    y: int
    operator: Operator
    status: Status
    created: datetime
    updated: datetime


class TaskDB(BaseTaskDB):
    """Объект задачи из хранилища"""

    id: int
    result: float | None = None

    class Config:  # pylint: disable=too-few-public-methods,missing-class-docstring
        orm_mode = True


class UpdateTaskDB(BaseModel):
    """Модель данных для функции обновления записи в базе данных"""

    id: int
    updated: datetime
    status: Status
    result: float | None
