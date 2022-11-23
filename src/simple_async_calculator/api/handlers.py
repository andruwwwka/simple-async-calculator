from fastapi import FastAPI, Path, status

from simple_async_calculator.entities.api.create_task import (
    CreateTaskRequest,
    CreateTaskResponse,
)
from simple_async_calculator.entities.api.task_detail import TaskDetailResponse
from simple_async_calculator.entities.api.tasks_listing import (
    TaskItem,
    TaskListingResponse,
)
from simple_async_calculator.entities.db.task import BaseTaskDB
from simple_async_calculator.enums.status import Status
from simple_async_calculator.services.calculator import calculate
from simple_async_calculator.storage.task import (
    create_task,
    get_task_by_id,
    get_tasks,
    update_task,
)

app = FastAPI()

MIN_AVAILABLE_TASK_ID: int = 1


@app.post(
    "/tasks",
    response_model=CreateTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task_service(task: CreateTaskRequest) -> CreateTaskResponse:
    """Сервис ручки создания задачи"""
    task_data = BaseTaskDB(
        status=Status.PENDING,
        **task.dict(),
    )
    task_id = create_task(task_data)
    return CreateTaskResponse(task_id=task_id)


@app.get("/tasks", response_model=TaskListingResponse)
async def tasks_listing_service() -> TaskListingResponse:
    """Сервис ручки листинга задач"""
    tasks = get_tasks()
    return TaskListingResponse(tasks=[TaskItem(**task.dict()) for task in tasks])


@app.get("/tasks/{task_id}", response_model=TaskDetailResponse)
async def task_detail_service(
    task_id: int = Path(description="Идентификатор задачи", ge=MIN_AVAILABLE_TASK_ID),
) -> TaskDetailResponse:
    """Сервис ручки получения результата задачи"""
    task = get_task_by_id(task_id)
    result = calculate(x=task.x, y=task.y, operator=task.operator)
    updated_task = update_task(task_id=task_id, result=result, status=Status.SUCCESS)
    return TaskDetailResponse(**updated_task.dict())
