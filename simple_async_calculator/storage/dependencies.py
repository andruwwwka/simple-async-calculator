from collections.abc import Generator

from simple_async_calculator.storage import async_session
from simple_async_calculator.storage.task import TaskDAL


async def get_task_dal() -> Generator[TaskDAL, None, None]:
    async with async_session() as session:
        async with session.begin():
            yield TaskDAL(session)
