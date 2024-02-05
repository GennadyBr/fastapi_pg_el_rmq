from logging import getLogger
from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

LOGGER = getLogger(__name__)

# create async engine
engine = create_async_engine(
    settings.REAL_DATABASE_URL,
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

# create session AssyncSession
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting AsyncSession"""
    # LOGGER.info("Getting database AsyncSession")
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
