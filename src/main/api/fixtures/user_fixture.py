import allure
import pytest

from src.main.api.classes.api_manager import APIManager
from src.main.api.fixtures.help_models import UserFixture
from src.main.api.foundation.protocols import UserFactory
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.fixture
def user_factory(api_manager: APIManager) -> UserFactory:
    def factory() -> UserFixture:
        with allure.step("Подготовка пользователя"):
            create_user_request = RandomModelGenerator.generate(CreateUserRequest)
            response = api_manager.admin_steps.create_user(create_user_request)

            return UserFixture(response=response, request=create_user_request)

    return factory


@pytest.fixture
def credit_user_factory(api_manager: APIManager) -> UserFactory:
    def factory() -> UserFixture:
        with allure.step("Подготовка пользователя с доступом к кредитам"):
            create_user_request = RandomModelGenerator.generate(CreateUserRequest).model_copy(
                update={"role": "ROLE_CREDIT_SECRET"}
            )
            response = api_manager.admin_steps.create_user(create_user_request)

            return UserFixture(response=response, request=create_user_request)

    return factory
