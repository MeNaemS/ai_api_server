import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models import Base
from src.config import config


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    db_url = f"postgresql+psycopg://{config.database.username}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}"
    engine = create_async_engine(db_url, echo=False)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def session_factory(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield factory
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(session_factory):
    async with session_factory() as session:
        yield session
        await session.rollback()
