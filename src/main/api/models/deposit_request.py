from typing import Annotated

from pydantic import Field

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import CamelCaseModel


class DepositRequest(CamelCaseModel):
    account_id: int = Field(alias="accountId")
    amount: Annotated[float, CreationRule(regex=r"^(?:[1-8]\d{3})\.\d{2}$")]
