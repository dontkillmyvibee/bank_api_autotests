from datetime import datetime

from sqlalchemy import Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = "credit"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return (f"Credit("
                f"id={self.id},"
                f" account_id={self.account_id},"
                f" amount={self.amount},"
                f"term_months={self.term_months},"
                f"balance={self.balance},"
                f"created_at={self.created_at})"
                )
