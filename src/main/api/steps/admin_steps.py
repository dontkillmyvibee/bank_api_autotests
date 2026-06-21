import allure

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validated_crud_requester import ValidatedCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AdminSteps(BaseSteps):
    @allure.step("Создание пользователя")
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidatedCrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.ADMIN_CREATE_USER,
        ).post(create_user_request)

        self.created_obj.append(response)
        return response

    @allure.step("Создание невалидного пользователя")
    def create_invalid_user(self, create_user_request: CreateUserRequest):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad(),
            endpoint=Endpoint.ADMIN_CREATE_USER,
        ).post(create_user_request)

    @allure.step("Удаление пользователя")
    def delete_user(self, user_id: int):
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.ADMIN_DELETE_USER
        ).delete(user_id)

    @allure.step("Авторизация пользователя")
    def login_user(self, login_user_request: LoginUserRequest):
        response = ValidatedCrudRequester(
            request_spec=RequestSpecs.unauth_headers(),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.LOGIN_USER
        ).post(login_user_request)
        return response
