from src.application.ports.auth_repository import AuthRepository
from src.domain.models.user import UserInDB, AuthUser, RegisterUser
from src.domain.models.token import Token
from src.infrastructure.security.password_hasher import PasswordHasher
from jwt import encode
from datetime import datetime, timedelta
from config.schema import Config
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, repo: AuthRepository, config: Config, hasher: PasswordHasher):
        self.repo: AuthRepository = repo
        self.config: Config = config
        self.hasher: PasswordHasher = hasher
        logger.info("AuthService initialized")

    async def login_user(self, user: AuthUser) -> Optional[Token]:
        logger.info(f"Login attempt for user: {user.login}")
        user_in_db: UserInDB = await self.repo.get_user_in_db_by_login(user.login)
        if not user_in_db or not await self.hasher.verify_password(user.password, user_in_db.password):
            logger.warning(f"Login failed: User not found: {user.login}")
            return
        logger.info(f"User {user.login} authenticated successfully")
        access_token = await self._create_access_token({"sub": user_in_db.id})
        logger.info(f"Access token created for user: {user.login}")
        return Token(
            access_token=access_token,
            token_type="bearer",
            expire=self.config.jwt.expire
        )

    async def register_user(self, user: RegisterUser) -> Token:
        logger.info(f"Registering new user: {user.login}")
        user_in_db: UserInDB = await self.repo.create_user_in_db(user)
        logger.info(f"User registered successfully: {user.login} with ID: {user_in_db.id}")
        access_token = await self._create_access_token({"sub": user_in_db.id})
        logger.info(f"Access token created for new user: {user.login}")
        return Token(
            access_token=access_token,
            token_type="bearer",
            expire=self.config.jwt.expire
        )

    async def _create_access_token(self, data: dict) -> str:
        logger.debug(f"Creating access token with payload: {data}")
        to_encode: dict = data.copy() | {
            "exp": datetime.now() + timedelta(minutes=self.config.jwt.expire)
        }
        encoded_jwt: str = encode(
            to_encode, self.config.jwt.secret_key, algorithm=self.config.jwt.algorithm
        )
        return encoded_jwt
