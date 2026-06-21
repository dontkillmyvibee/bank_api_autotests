import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import APIManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.foundation.protocols import AccountFactory, UserFactory
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.repay_request import RepayRequest


@pytest.mark.api
class TestCredit:
    def test_credit_request_valid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            credit_user_factory: UserFactory
    ):
        account = account_factory(credit_user_factory())
        credit_request = CreditRequest(
            account_id=account.response.id,
            amount=5000,
            term_months=12
        )

        response = api_manager.user_steps.request_credit(
            create_user=account.user.request,
            credit_request=credit_request
        )

        assert response.id == account.response.id
        assert response.amount == credit_request.amount
        assert response.term_months == credit_request.term_months
        assert response.balance == account.response.balance + credit_request.amount

        credit_from_db = CreditCrudDb.get_credit_by_id(db_session, response.credit_id)
        assert credit_from_db is not None, "Кредит не создан в БД"
        assert credit_from_db.account_id == account.response.id
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.term_months
        assert credit_from_db.balance == -credit_request.amount, "Долг по кредиту в БД некорректен"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.response.id)
        assert account_from_db.balance == response.balance, "Баланс в БД не соответствует ответу API"
        assert account_from_db.balance == account.response.balance + credit_request.amount, \
            "Сумма кредита не зачислена на счёт в БД"

    def test_credit_request_invalid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            credit_user_factory: UserFactory
    ):
        account = account_factory(credit_user_factory())
        credit_request = CreditRequest(
            account_id=account.response.id,
            amount=-100,
            term_months=12
        )

        api_manager.user_steps.request_credit_invalid(
            create_user=account.user.request,
            credit_request=credit_request
        )

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.response.id)
        assert account_from_db.balance == account.response.balance, \
            "Баланс изменился после неудачного запроса кредита"

        credits_from_db = CreditCrudDb.get_credits_by_account_id(db_session, account.response.id)
        assert credits_from_db == [], "Кредит создан в БД при некорректном запросе"

    def test_credit_repay_valid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            credit_user_factory: UserFactory
    ):
        account = account_factory(credit_user_factory())
        credit = api_manager.user_steps.request_credit(
            create_user=account.user.request,
            credit_request=CreditRequest(
                account_id=account.response.id,
                amount=5000,
                term_months=12
            )
        )

        credit_before = CreditCrudDb.get_credit_by_id(db_session, credit.credit_id)
        credit_balance_before = credit_before.balance
        account_balance_before = credit.balance

        repay_amount = 5000
        repay_response = api_manager.user_steps.repay_credit(
            create_user=account.user.request,
            repay_request=RepayRequest(
                credit_id=credit.credit_id,
                account_id=account.response.id,
                amount=repay_amount
            )
        )

        assert repay_response.credit_id == credit.credit_id
        assert repay_response.amount_deposited == repay_amount

        db_session.expire_all()

        credit_after = CreditCrudDb.get_credit_by_id(db_session, credit.credit_id)
        assert credit_after.balance == credit_balance_before + repay_amount, \
            "Долг по кредиту в БД не уменьшился на сумму погашения"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.response.id)
        assert account_from_db.balance == account_balance_before - repay_amount, \
            "Баланс счёта в БД не уменьшился на сумму погашения"

    def test_credit_repay_invalid(
            self,
            db_session: Session,
            api_manager: APIManager,
            account_factory: AccountFactory,
            credit_user_factory: UserFactory
    ):
        account = account_factory(credit_user_factory())
        credit = api_manager.user_steps.request_credit(
            create_user=account.user.request,
            credit_request=CreditRequest(
                account_id=account.response.id,
                amount=5000,
                term_months=12
            )
        )

        credit_before = CreditCrudDb.get_credit_by_id(db_session, credit.credit_id)
        credit_balance_before = credit_before.balance
        account_balance_before = credit.balance

        api_manager.user_steps.repay_credit_invalid(
            create_user=account.user.request,
            repay_request=RepayRequest(
                credit_id=credit.credit_id,
                account_id=account.response.id,
                amount=-100
            )
        )

        db_session.expire_all()

        credit_after = CreditCrudDb.get_credit_by_id(db_session, credit.credit_id)
        assert credit_after.balance == credit_balance_before, \
            "Долг по кредиту изменился после неудачного погашения"

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.response.id)
        assert account_from_db.balance == account_balance_before, \
            "Баланс счёта изменился после неудачного погашения"
