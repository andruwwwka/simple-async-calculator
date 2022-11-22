import logging

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
    """Сервис ручки создания задачи"""
    logging.debug(task_request)
    return CreateTaskResponse(task_id=1)


@app.get("/tasks")
async def tasks_listing() -> TaskListingResponse:
    """Сервис ручки листинга задач"""
    return TaskListingResponse(tasks=[TaskItem(id=1, status=Status.PENDING)])


@app.get("/tasks/{task_id}")
async def task_detail(task_id: int) -> TaskDetailResponse:
    """Сервис ручки получения результата задачи"""
    logging.debug(task_id)
    return TaskDetailResponse(
        status=Status.PENDING,
        result=None,
    )
