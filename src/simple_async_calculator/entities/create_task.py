from pydantic import BaseModel

from simple_async_calculator.enums.operator import Operator


class CreateTaskRequest(BaseModel):
    x: int
    y: int
    operator: Operator


class CreateTaskResponse(BaseModel):
    task_id: int
