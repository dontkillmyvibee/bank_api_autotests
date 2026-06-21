from pydantic import Field

from src.main.api.models.base_model import CamelCaseModel


class RepayRequest(CamelCaseModel):
    credit_id: int = Field(alias="creditId")
    account_id: int = Field(alias="accountId")
    amount: float
