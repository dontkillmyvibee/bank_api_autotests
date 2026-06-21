from sqlalchemy import Integer, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.main.api.db.base import Base


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    balance: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, user_id={self.user_id}, number={self.number}, balance={self.balance})"
