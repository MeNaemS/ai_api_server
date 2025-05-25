from abc import ABC, abstractmethod
from src.domain.models.user import UserInDB, RegisterUser


class AuthRepository(ABC):
    @abstractmethod
    async def get_user_in_db_by_login(self, login: str) -> UserInDB:
        ...

    @abstractmethod
    async def create_user_in_db(self, user: RegisterUser) -> UserInDB:
        ...
