from collections.abc import AsyncGenerator

from simple_async_calculator.storage import async_session
from simple_async_calculator.storage.task import TaskDAL


async def get_task_dal() -> AsyncGenerator[TaskDAL, None]:
    """Зависимость, возвращающая объект слоя доступа к данным"""
    async with async_session() as session:
        async with session.begin():
            yield TaskDAL(session)
