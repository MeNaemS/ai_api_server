from src.application.ports.auth_repository import AuthRepository
from src.domain.models.user import UserInDB, RegisterUser
from src.infrastructure.security.password_hasher import PasswordHasher
import asyncpg
import logging

logger = logging.getLogger(__name__)


class AsyncPGAuthRepository(AuthRepository):
    def __init__(self, pool: asyncpg.Pool, hasher: PasswordHasher):
        self.pool: asyncpg.Pool = pool
        self.hasher: PasswordHasher = hasher
        logger.info("AsyncPGAuthRepository initialized")

    async def get_user_in_db_by_login(self, login: str) -> UserInDB:
        logger.info(f"Attempting to get user by login: {login}")
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM "Users" WHERE login = $1', login)
            if row:
                logger.info(f"User found with login: {login}")
                return UserInDB(**row)
            logger.info(f"No user found with login: {login}")
            return None

    async def create_user_in_db(self, user: RegisterUser) -> UserInDB:
        logger.info(f"Creating new user with login: {user.login}")
        hashed_password: str = await self.hasher.password_hash(user.password)
        async with self.pool.acquire() as conn:
            if user.full_name:
                logger.info("Creating full name record for user")
                full_name_id: int = await conn.fetchval(
                    'INSERT INTO "FullName" (name, surname, patronymic) VALUES ($1, $2, $3) RETURNING id',
                    user.full_name.name,
                    user.full_name.surname,
                    user.full_name.patronymic
                )
                logger.info(f"Full name record created with ID: {full_name_id}")
            
            logger.info(f"Inserting user record for {user.login}")
            row = await conn.fetchrow(
                'INSERT INTO "Users" (login, email, full_name, password) VALUES ($1, $2, $3, $4) RETURNING *',
                user.login,
                user.email,
                user.full_name if not user.full_name else full_name_id,
                hashed_password,
            )
            logger.info(f"User created successfully with ID: {row['id']}")
            return UserInDB(**row)

