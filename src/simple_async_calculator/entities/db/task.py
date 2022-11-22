from pydantic import BaseModel

from simple_async_calculator.enums.operator import Operator
from simple_async_calculator.enums.status import Status


class Task(BaseModel):
    """Объект задачи из хранилища"""

    id: int
    x: int
    y: int
    operator: Operator
    status: Status
    result: float | None = None
