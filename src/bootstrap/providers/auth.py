from dishka import Provider, provide, Scope
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from src.config_schema import Config
from src.infrastructure.security.password_hasher import PasswordHasher
from src.infrastructure.database.auth_repo import AsyncPGAuthRepository
from src.application.usecases.auth_user_case import AuthService
from src.infrastructure.mappers.token import TokenMapper


class AuthContainer(Provider):
    @provide(scope=Scope.APP)
    async def password_hasher(self) -> PasswordHasher:
        return PasswordHasher()

    @provide(scope=Scope.APP)
    async def auth_service(
        self,
        repo: AsyncPGAuthRepository,
        config: Config,
        hasher: PasswordHasher,
        token_mapper: TokenMapper
    ) -> AuthService:
        return AuthService(repo, config, hasher, token_mapper)

    @provide(scope=Scope.APP)
    async def auth_repository(
        self,
        session: sessionmaker[AsyncSession],
        hasher: PasswordHasher
    ) -> AsyncPGAuthRepository:
        return AsyncPGAuthRepository(session, hasher)
