from fastapi import FastAPI, Path, status

from simple_async_calculator.entities.api.create_task import (
    CreateTaskRequest,
    CreateTaskResponse,
)
from simple_async_calculator.entities.api.task_detail import TaskDetailResponse
from simple_async_calculator.entities.api.tasks_listing import TaskItem, TaskListingResponse
from simple_async_calculator.entities.db.task import Task
from simple_async_calculator.enums.status import Status
from simple_async_calculator.services.calculator import calculate

app = FastAPI()

MIN_AVAILABLE_TASK_ID: int = 1

TASKS_CONTAINER: list = []


@app.post(
    "/tasks",
    response_model=CreateTaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(task: CreateTaskRequest) -> CreateTaskResponse:
    """Сервис ручки создания задачи"""
    task_id = len(TASKS_CONTAINER) + 1
    TASKS_CONTAINER.append(
        Task(
            id=task_id,
            status=Status.PENDING,
            **task.dict(),
        )
    )
    return CreateTaskResponse(task_id=task_id)


@app.get("/tasks", response_model=TaskListingResponse)
async def tasks_listing() -> TaskListingResponse:
    """Сервис ручки листинга задач"""
    return TaskListingResponse(tasks=[TaskItem(**task.dict()) for task in TASKS_CONTAINER])


@app.get("/tasks/{task_id}", response_model=TaskDetailResponse)
async def task_detail(
    task_id: int = Path(description="Идентификатор задачи", ge=MIN_AVAILABLE_TASK_ID),
) -> TaskDetailResponse:
    """Сервис ручки получения результата задачи"""
    task: Task = next(filter(lambda tsk: tsk.id == task_id, TASKS_CONTAINER))
    result = calculate(x=task.x, y=task.y, operator=task.operator)
    task.result = result
    task.status = Status.SUCCESS
    TASKS_CONTAINER[task_id - 1] = task
    return TaskDetailResponse(**task.dict())
