from pydantic import Field

from src.main.api.models.base_model import CamelCaseModel


class CreditResponse(CamelCaseModel):
    id: int
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    credit_id: int = Field(alias="creditId")
