import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from simple_async_calculator.api.handlers import app
from simple_async_calculator.settings import settings
from simple_async_calculator.storage import Base
from simple_async_calculator.storage.dependencies import get_task_dal
from simple_async_calculator.storage.task import TaskDAL


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def engine():
    engine = create_async_engine(
        (
            "postgresql+asyncpg://"
            f"{settings.db_user}:"
            f"{settings.db_password}@"
            f"{settings.db_host}"
            ":5432/"
            f"{settings.db_name}"
        )
    )
    yield engine
    await engine.dispose()


@pytest.fixture(autouse=True)
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def async_session(engine):
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture
def override_dependency(async_session):
    async def override_get_task_dal():
        async with async_session() as session:
            async with session.begin():
                yield TaskDAL(session)

    return override_get_task_dal


@pytest.fixture
async def client(override_dependency):
    app.dependency_overrides[get_task_dal] = override_dependency
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
