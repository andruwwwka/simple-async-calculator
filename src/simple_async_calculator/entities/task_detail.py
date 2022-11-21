from pydantic import BaseModel

from simple_async_calculator.enums.status import Status


class TaskDetailResponse(BaseModel):
    status: Status
    result: float | None = None