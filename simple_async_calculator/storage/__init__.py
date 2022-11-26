from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from simple_async_calculator.settings import settings

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

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def setup():
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
