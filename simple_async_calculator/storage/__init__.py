from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from simple_async_calculator.settings import settings


def database_connection_string() -> str:
    """Создание URI для подключения к базе данных"""
    return (
        "postgresql+asyncpg://"
        f"{settings.db_user}:"
        f"{settings.db_password}@"
        f"{settings.db_host}"
        ":5432/"
        f"{settings.db_name}"
    )


engine = create_async_engine(database_connection_string())

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def setup():  # pragma: no cover
    """Создание базы данных при запуске приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
