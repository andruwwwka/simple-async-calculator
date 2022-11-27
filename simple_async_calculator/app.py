import aiocron
from fastapi import FastAPI

from simple_async_calculator.api.handlers import task_router
from simple_async_calculator.services.cron import cron_service
from simple_async_calculator.storage import setup

app = FastAPI()

app.include_router(task_router)


@app.on_event("startup")
async def startup():  # pragma: no cover
    """Дополнительные действия, необходимые при старте приложения"""
    await setup()


@aiocron.crontab("* * * * */30")
async def calculate_tasks():  # pragma: no cover
    """Объявление крон-задачи для расчета результатов.

    Запускается 1 раз в 30 секунд"""
    await cron_service()
