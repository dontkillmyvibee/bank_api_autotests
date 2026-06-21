from pydantic import Field

from src.main.api.models.base_model import CamelCaseModel


class TransferResponse(CamelCaseModel):
    from_account_id: int = Field(alias="fromAccountId")
    to_account_id: int = Field(alias="toAccountId")
    from_account_id_balance: float = Field(alias="fromAccountIdBalance")
