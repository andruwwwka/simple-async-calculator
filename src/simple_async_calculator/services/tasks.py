from fastapi import FastAPI

from simple_async_calculator.entities.create_task import (
    CreateTaskRequest,
    CreateTaskResponse,
)
from simple_async_calculator.entities.task_detail import TaskDetailResponse
from simple_async_calculator.entities.tasks_listing import TaskItem, TaskListingResponse
from simple_async_calculator.enums.status import Status

app = FastAPI()


@app.post("/tasks")
async def create_task(task_request: CreateTaskRequest) -> CreateTaskResponse:
    return CreateTaskResponse(task_id=1)


@app.get("/tasks")
async def tasks_listing() -> TaskListingResponse:
    return TaskListingResponse(tasks=[TaskItem(id=1, status=Status.pending)])


@app.get("/tasks/{task_id}")
async def task_detail(task_id: int) -> TaskDetailResponse:
    return TaskDetailResponse(
        status=Status.pending,
        result=None,
    )
