import allure

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    @allure.step("Создание банковского счёта")
    def create_account(self, create_user: CreateUserRequest) -> CreateAccountResponse:
        response = ValidatedCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_created(),
            endpoint=Endpoint.CREATE_ACCOUNT
        ).post()
        return response

    @allure.step("Пополнение счёта")
    def deposit(self, create_user: CreateUserRequest, deposit_request: DepositRequest):
        response = ValidatedCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.DEPOSIT
        ).post(deposit_request)
        return response

    @allure.step("Невалидное пополнение счёта")
    def deposit_invalid(self, create_user: CreateUserRequest, deposit_request: DepositRequest):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_bad(),
            endpoint=Endpoint.DEPOSIT
        ).post(deposit_request)

    @allure.step("Перевод между счетами")
    def transfer(self, create_user: CreateUserRequest, transfer_request: TransferRequest) -> TransferResponse:
        response = ValidatedCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.TRANSFER
        ).post(transfer_request)
        return response

    @allure.step("Невалидный перевод между счетами")
    def transfer_invalid(self, create_user: CreateUserRequest, transfer_request: TransferRequest):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_unprocessable(),
            endpoint=Endpoint.TRANSFER
        ).post(transfer_request)

    @allure.step("Запрос на получение кредита")
    def request_credit(self, create_user: CreateUserRequest, credit_request: CreditRequest) -> CreditResponse:
        response = ValidatedCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_created(),
            endpoint=Endpoint.CREDIT_REQUEST
        ).post(credit_request)
        return response

    @allure.step("Невалидный запрос на получение кредита")
    def request_credit_invalid(self, create_user: CreateUserRequest, credit_request: CreditRequest):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_bad(),
            endpoint=Endpoint.CREDIT_REQUEST
        ).post(credit_request)

    @allure.step("Погашение кредита")
    def repay_credit(self, create_user: CreateUserRequest, repay_request: RepayRequest) -> RepayResponse:
        response = ValidatedCrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.CREDIT_REPAY
        ).post(repay_request)
        return response

    @allure.step("Невалидное погашение кредита")
    def repay_credit_invalid(self, create_user: CreateUserRequest, repay_request: RepayRequest):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(
                username=create_user.username,
                password=create_user.password
            ),
            response_spec=ResponseSpecs.request_bad(),
            endpoint=Endpoint.CREDIT_REPAY
        ).post(repay_request)
