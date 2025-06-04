from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class Base(DeclarativeBase, MappedAsDataclass):
    pass


from src.infrastructure.database.models.users import User
from src.infrastructure.database.models.ai_info import AIInfo
from src.infrastructure.database.models.chat import Chat, ChatHistory
