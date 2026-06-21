from typing import Callable

import allure
import pytest

from src.main.api.classes.api_manager import APIManager
from src.main.api.fixtures.help_models import AccountFixture, UserFixture
from src.main.api.foundation.protocols import AccountFactory
from src.main.api.models.deposit_request import DepositRequest


@pytest.fixture
def account_factory(api_manager: APIManager, user_factory: Callable) -> AccountFactory:
    def factory(user: UserFixture | None = None) -> AccountFixture:
        with allure.step("Подготовка счёта"):
            if user is None:
                user = user_factory()

            response = api_manager.user_steps.create_account(user.request)

            return AccountFixture(user=user, response=response)

    return factory


@pytest.fixture
def account_factory_with_deposit(api_manager: APIManager, user_factory: Callable) -> AccountFactory:
    def factory(user: UserFixture | None = None) -> AccountFixture:
        with allure.step("Подготовка счёта с депозитом"):
            if user is None:
                user = user_factory()

            response = api_manager.user_steps.create_account(user.request)
            deposit_response = api_manager.user_steps.deposit(
                create_user=user.request,
                deposit_request=DepositRequest(account_id=response.id, amount=8000)
            )
            response.balance = deposit_response.balance
            return AccountFixture(user=user, response=response)

    return factory
