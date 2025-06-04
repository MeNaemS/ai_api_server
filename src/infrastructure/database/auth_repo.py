from src.domain.models.user import RegisterUser
from src.infrastructure.database.models.users import User
from src.infrastructure.security.password_hasher import PasswordHasher
import logging
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert

logger = logging.getLogger(__name__)


class AsyncPGAuthRepository:
    def __init__(self, session: sessionmaker[AsyncSession], hasher: PasswordHasher):
        self.session: sessionmaker[AsyncSession] = session
        self.hasher: PasswordHasher = hasher
        logger.info("AsyncPGAuthRepository initialized")

    async def get_user_in_db_by_login(self, login: str) -> Optional[User]:
        logger.info(f"Attempting to get user by login: {login}")
        async with self.session() as session:
            result = await session.execute(select(User).where(User.login == login))
            user = result.scalar_one_or_none()
            if user:
                logger.info(f"User found with login: {login}")
                return user
            logger.info(f"No user found with login: {login}")
            return

    async def create_user_in_db(self, new_user: RegisterUser) -> User:
        logger.info(f"Creating new user with login: {new_user.login}")
        hashed_password: str = await self.hasher.password_hash(new_user.password)
        async with self.session() as session:
            logger.info("Checking if user already exists")
            user = await session.execute(select(User).where(User.login == new_user.login))
            if user.scalar_one_or_none():
                logger.info(f"User with login {new_user.login} already exists")
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Login already exists"
                )
            logger.info(f"Inserting user record for {new_user.login}")
            if new_user.full_name:
                user = await session.execute(
                    insert(User).values(
                        login=new_user.login,
                        email=new_user.email,
                        name=new_user.full_name.name,
                        surname=new_user.full_name.surname,
                        patronymic=new_user.full_name.patronymic,
                        password=hashed_password
                    ).returning(User)
                )
            else:
                user = await session.execute(
                    insert(User).values(
                        login=new_user.login,
                        email=new_user.email,
                        password=hashed_password
                    ).returning(User)
                )
            user = user.scalar_one()
            logger.info(f"User created successfully with ID: {user.id}")
            await session.commit()
            return user
