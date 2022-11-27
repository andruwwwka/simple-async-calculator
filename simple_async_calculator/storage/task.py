from sqlalchemy import select, update
from sqlalchemy.orm import Session

from simple_async_calculator.entities.db import BaseTaskDB, UpdateTaskDB
from simple_async_calculator.enums.status import Status
from simple_async_calculator.storage.tables import Task


class TaskDAL:
    """Описание методов слоя доступа к данным"""

    def __init__(self, db_session: Session) -> None:
        """Создание объекта слоя доступа к данным"""
        self.db_session = db_session

    async def create(self, task: BaseTaskDB) -> Task:
        """Создание в базе данных записи с задачей"""
        new_task = Task(
            **task.dict(),
        )
        self.db_session.add(new_task)
        await self.db_session.flush()
        return new_task

    async def get_one(self, task_id: int) -> Task:
        """Получение задачи из базы данных по ID"""
        task = await self.db_session.execute(select(Task).where(Task.id == task_id))
        return task.scalar()

    async def get_all(self, status: Status | None = None) -> list[Task]:
        """Получение всех задачи из базы данных"""
        stmt = select(Task)
        if status:
            stmt = stmt.where(Task.status == status.value)
        tasks = await self.db_session.execute(stmt)
        return tasks.scalars().all()

    async def update(self, task_data: UpdateTaskDB) -> Task:
        """Обновление задачи в базе данных"""
        stmt = (
            update(Task)
            .where(Task.id == task_data.id)
            .values(
                updated=task_data.updated,
                status=task_data.status,
            )
        )
        if task_data.result is not None:
            stmt = stmt.values(result=task_data.result)
        task = await self.db_session.execute(stmt.returning(Task))
        return task.scalar()
