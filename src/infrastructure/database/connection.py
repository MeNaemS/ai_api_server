import asyncpg
from config.schema import Config


async def create_pool(config: Config) -> asyncpg.Pool:
    return await asyncpg.create_pool(
        user=config.database.username,
        password=config.database.password,
        database=config.database.database,
        host=config.database.host,
        port=config.database.port,
    )
