import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import APIManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.foundation.protocols import AccountFactory
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestDeposit:
    @pytest.mark.parametrize(
        "deposit_request",
        [RandomModelGenerator.generate(DepositRequest)]
    )
    def test_deposit_valid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            deposit_request: DepositRequest
    ):
        account = account_factory()
        deposit_request = deposit_request.model_copy(
            update={"account_id": account.response.id}
        )

        response = api_manager.user_steps.deposit(
            account.user.request,
            deposit_request
        )

        assert response.id == account.response.id
        assert response.balance == account.response.balance + deposit_request.amount

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.response.id)

        assert account_from_db.balance == response.balance, "Баланс в БД не соответствует ответу API"
        assert account_from_db.balance == deposit_request.amount, "Сумма депозита не зачислена в БД"

    @pytest.mark.parametrize("amount", [-100])
    def test_deposit_invalid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            amount: float
    ):
        account = account_factory()
        deposit_request = DepositRequest(
            account_id=account.response.id,
            amount=amount
        )

        api_manager.user_steps.deposit_invalid(account.user.request, deposit_request)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.response.id)

        assert account_from_db.balance == account.response.balance, \
            "Баланс изменился после неудачного депозита"
