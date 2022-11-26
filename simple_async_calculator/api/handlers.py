from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Path, status

from simple_async_calculator.entities.api.create_task import (
    CreateTaskRequest,
    CreateTaskResponse,
)
from simple_async_calculator.entities.api.task_detail import TaskDetailResponse
from simple_async_calculator.entities.api.tasks_listing import TaskListingResponse
from simple_async_calculator.entities.db import BaseTaskDB
from simple_async_calculator.enums.status import Status
from simple_async_calculator.services.calculator import calculate
from simple_async_calculator.storage import setup
from simple_async_calculator.storage.dependencies import get_task_dal
from simple_async_calculator.storage.task import TaskDAL

app = FastAPI()

MIN_AVAILABLE_TASK_ID: int = 1


@app.on_event("startup")
async def startup():  # pragma: no cover
    """Дополнительные действия, необходимые при старте приложения"""
    await setup()


@app.post(
    "/tasks",
    response_model=CreateTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_service(
    task: CreateTaskRequest, task_dal: TaskDAL = Depends(get_task_dal)
) -> CreateTaskResponse:
    """Сервис ручки создания задачи"""
    now = datetime.now(timezone.utc)
    task_data = BaseTaskDB(
        created=now,
        updated=now,
        status=Status.PENDING,
        **task.dict(),
    )
    created_task = await task_dal.create(task_data)
    return created_task


@app.get("/tasks", response_model=TaskListingResponse)
async def tasks_listing_service(
    task_dal: TaskDAL = Depends(get_task_dal),
) -> TaskListingResponse:
    """Сервис ручки листинга задач"""
    tasks = await task_dal.get_all()
    return TaskListingResponse(tasks=tasks)


@app.get("/tasks/{task_id}", response_model=TaskDetailResponse)
async def task_detail_service(
    task_id: int = Path(description="Идентификатор задачи", ge=MIN_AVAILABLE_TASK_ID),
    task_dal: TaskDAL = Depends(get_task_dal),
) -> TaskDetailResponse:
    """Сервис ручки получения результата задачи"""
    _task = await task_dal.get_one(task_id)
    if _task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    result = calculate(x=_task.x, y=_task.y, operator=_task.operator)
    await task_dal.update(task_id=task_id, result=result, status=Status.SUCCESS)
    task = await task_dal.get_one(task_id)
    return task
