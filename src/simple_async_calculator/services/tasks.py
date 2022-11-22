import logging

from fastapi import FastAPI, Path, status

from simple_async_calculator.entities.create_task import (
    CreateTaskRequest,
    CreateTaskResponse,
)
from simple_async_calculator.entities.task_detail import TaskDetailResponse
from simple_async_calculator.entities.tasks_listing import TaskItem, TaskListingResponse
from simple_async_calculator.enums.status import Status

app = FastAPI()


MIN_AVAILABLE_TASK_ID: int = 1


@app.post(
    "/tasks",
    response_model=CreateTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(task: CreateTaskRequest) -> CreateTaskResponse:
    """Сервис ручки создания задачи"""
    logging.debug(task)
    return CreateTaskResponse(task_id=1)


@app.get("/tasks", response_model=TaskListingResponse)
async def tasks_listing() -> TaskListingResponse:
    """Сервис ручки листинга задач"""
    return TaskListingResponse(tasks=[TaskItem(id=1, status=Status.PENDING)])


@app.get("/tasks/{task_id}", response_model=TaskDetailResponse)
async def task_detail(
        task_id: int = Path(description="Идентификатор задачи", ge=MIN_AVAILABLE_TASK_ID),
) -> TaskDetailResponse:
    """Сервис ручки получения результата задачи"""
    logging.debug(task_id)
    return TaskDetailResponse(
        status=Status.PENDING,
        result=None,
    )
