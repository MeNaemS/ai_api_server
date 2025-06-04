from dishka import Provider, Scope, provide
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from src.config_schema import Config
from src.infrastructure.database.connection import create_session


class Container(Provider):
    @provide(scope=Scope.APP)
    def app_config(self) -> Config:
        return config

    @provide(scope=Scope.APP)
    async def get_session(self, config: Config) -> sessionmaker[AsyncSession]:
        return await create_session(config)
