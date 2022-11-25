from sqlalchemy import select, update
from sqlalchemy.orm import Session

from simple_async_calculator.entities.db import BaseTaskDB
from simple_async_calculator.enums.status import Status
from simple_async_calculator.storage.tables import Task


class TaskDAL:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    async def create(self, task: BaseTaskDB):
        new_task = Task(
            **task.dict(),
        )
        self.db_session.add(new_task)
        await self.db_session.flush()
        return new_task

    async def get_one(self, task_id):
        task = await self.db_session.execute(select(Task).where(Task.id == task_id))
        return task.scalar()

    async def get_all(self):
        tasks = await self.db_session.execute(select(Task))
        return tasks.scalars().all()

    async def update(self, *, task_id: int, result: float, status: Status):
        task = await self.db_session.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(result=result, status=status)
            .returning(Task)
        )
        return task.scalar()
