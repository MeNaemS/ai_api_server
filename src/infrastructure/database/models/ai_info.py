from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean
from src.infrastructure.database.models import Base


class AIInfo(Base):
    __tablename__ = "AIInfo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    system_prompt: Mapped[str] = mapped_column(String, nullable=True)
    model: Mapped[str] = mapped_column(String, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
    top_p: Mapped[float] = mapped_column(Float, nullable=False, default=0.8)
    stream: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    chat = relationship("Chat", back_populates="ai_config")
