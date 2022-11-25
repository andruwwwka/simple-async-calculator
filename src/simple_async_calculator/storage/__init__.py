from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from simple_async_calculator.settings import settings

engine = create_async_engine(
    (
        "postgresql+asyncpg://"
        f"{settings.db_user}:"
        f"{settings.db_password}@localhost:5432/"
        f"{settings.db_name}"
    )
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
