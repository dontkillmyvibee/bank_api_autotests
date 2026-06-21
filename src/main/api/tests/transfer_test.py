import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import APIManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.foundation.protocols import AccountFactory
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer_valid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            account_factory_with_deposit: AccountFactory
    ):
        from_account = account_factory_with_deposit()
        to_account = account_factory(from_account.user)
        transfer_request = TransferRequest(
            to_account_id=to_account.response.id,
            from_account_id=from_account.response.id
        )
        response = api_manager.user_steps.transfer(
            create_user=to_account.user.request,
            transfer_request=transfer_request
        )

        assert response.from_account_id_balance == from_account.response.balance - transfer_request.amount

        account_from_db = AccountCrudDb.get_account_by_id(db_session, from_account.response.id)
        account_to_db = AccountCrudDb.get_account_by_id(db_session, to_account.response.id)

        assert account_from_db.balance == from_account.response.balance - transfer_request.amount
        assert account_to_db.balance == to_account.response.balance + transfer_request.amount

    def test_transfer_invalid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            account_factory_with_deposit: AccountFactory
    ):
        from_account = account_factory_with_deposit()
        to_account = account_factory(from_account.user)

        transfer_request = TransferRequest(
            to_account_id=to_account.response.id,
            from_account_id=from_account.response.id,
            amount=from_account.response.balance + 1000
        )
        api_manager.user_steps.transfer_invalid(
            create_user=from_account.user.request,
            transfer_request=transfer_request
        )

        account_from_db = AccountCrudDb.get_account_by_id(db_session, from_account.response.id)
        account_to_db = AccountCrudDb.get_account_by_id(db_session, to_account.response.id)

        assert account_from_db.balance == from_account.response.balance
        assert account_to_db.balance == to_account.response.balance
