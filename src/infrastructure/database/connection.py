from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from src.config_schema import Config


async def create_session(config: Config) -> sessionmaker[AsyncSession]:
    engine: AsyncEngine = create_async_engine(
        (
            f"postgresql+psycopg://{config.database.username}:{config.database.password}@"
            f"{config.database.host}:{config.database.port}/{config.database.database}"
        )
    )
    session: sessionmaker[AsyncSession] = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    return session
