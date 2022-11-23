from pydantic import BaseModel

from simple_async_calculator.enums.operator import Operator
from simple_async_calculator.enums.status import Status


class BaseTaskDB(BaseModel):
    """Объект задачи для создания сущности в хранилище"""

    x: int
    y: int
    operator: Operator
    status: Status


class TaskDB(BaseTaskDB):
    """Объект задачи из хранилища"""

    id: int
    result: float | None = None
