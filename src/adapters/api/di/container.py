from typing import AsyncGenerator
from dishka import Provider, Scope, provide
import asyncpg
from config.config import config
from config.schema import Config
from src.infrastructure.database.connection import create_pool
from src.infrastructure.security.password_hasher import PasswordHasher
from src.infrastructure.database.auth_repo import AsyncPGAuthRepository
from src.application.user_cases.auth_user_case import AuthService


class Container(Provider):
    @provide(scope=Scope.APP)
    def app_config(self) -> Config:
        return config

    @provide(scope=Scope.APP)
    async def get_pool(self, config: Config) -> AsyncGenerator[asyncpg.Pool, None]:
        pool: asyncpg.Pool = await create_pool(config)
        try:
            yield pool
        finally:
            await pool.close()

    @provide(scope=Scope.APP)
    async def password_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.APP)
    async def AuthService(self, repo: AsyncPGAuthRepository, config: Config, hasher: PasswordHasher) -> AuthService:
        return AuthService(repo, config, hasher)

    @provide(scope=Scope.APP)
    async def AuthRepository(self, pool: asyncpg.Pool, hasher: PasswordHasher) -> AsyncPGAuthRepository:
        return AsyncPGAuthRepository(pool, hasher)
