from pydantic import BaseModel

from simple_async_calculator.enums.status import Status


class TaskItem(BaseModel):
    id: int
    status: Status


class TaskListingResponse(BaseModel):
    tasks: list[TaskItem]
