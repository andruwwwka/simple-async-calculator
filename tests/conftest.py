# pylint: disable=redefined-outer-name
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from simple_async_calculator.api.handlers import app
from simple_async_calculator.storage import Base, database_connection_string
from simple_async_calculator.storage.dependencies import get_task_dal
from simple_async_calculator.storage.task import TaskDAL


@pytest.fixture
def anyio_backend():
    """Говорим anyio, что не используем trio"""
    return "asyncio"


@pytest.fixture
async def engine():
    """Коннектимся к базе данных перед тестом и сбрасываем соединение после теста"""
    engine = create_async_engine(database_connection_string())
    yield engine
    await engine.dispose()


@pytest.fixture(autouse=True)
async def create(engine):
    """Создание таблиц до теста и удаление после"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def async_session(engine):
    """Фикстура сессии к базе данных"""
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
def override_dependency(async_session):
    """Переопределяем в зависимости сессию на тестовую"""

    async def override_get_task_dal():
        async with async_session() as session:
            async with session.begin():
                yield TaskDAL(session)

    return override_get_task_dal


@pytest.fixture
async def client(override_dependency):
    """Клиент для API"""
    app.dependency_overrides[get_task_dal] = override_dependency
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
