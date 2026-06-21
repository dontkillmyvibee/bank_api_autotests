from pydantic import Field

from src.main.api.models.base_model import CamelCaseModel


class TransferRequest(CamelCaseModel):
    from_account_id: int = Field(alias="fromAccountId")
    to_account_id: int = Field(alias="toAccountId")
    amount: float = Field(default=500.50)
