from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from src.infrastructure.database.models import Base


class Chat(Base):
    __tablename__ = "Chat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    
    ai_config_id: Mapped[int] = mapped_column(ForeignKey("AIInfo.id"), nullable=False)

    ai_config = relationship("AIInfo", back_populates="chat")
    chat_history = relationship("ChatHistory", back_populates="chat")


class ChatHistory(Base):
    __tablename__ = "ChatHistory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(String, nullable=False)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("Chat.id"), nullable=False)
    
    author = relationship("User", back_populates="chat_history")
    chat = relationship("Chat", back_populates="chat_history")
