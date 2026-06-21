from datetime import datetime

from sqlalchemy import Integer, ForeignKey, Float, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.main.api.db.base import Base


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    to_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"))
    from_account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"), nullable=True)
    credit_id: Mapped[int] = mapped_column(Integer, ForeignKey("credit.id"), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __repr__(self) -> str:
        return (f"Transaction("
                f"id={self.id},"
                f"to_account_id={self.to_account_id},"
                f"from_account_id={self.from_account_id},"
                f"credit_id={self.credit_id},"
                f"amount={self.amount},"
                f"transaction_type={self.transaction_type},"
                f"created_at={self.created_at})"
                )
