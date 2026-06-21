from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.main.api.db.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, role={self.role}, deleted_at={self.deleted_at})"
