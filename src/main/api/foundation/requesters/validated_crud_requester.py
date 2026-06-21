from typing import Callable

import allure

from src.main.api.configs.config import Config
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.http_requester import HTTPRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel


class ValidatedCrudRequester(HTTPRequester):
    def __init__(self, request_spec: dict[str, str] | None, response_spec: Callable, endpoint: Endpoint):
        super().__init__(request_spec, response_spec, endpoint)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            response_spec=response_spec,
            endpoint=endpoint
        )

    def post(self, base_model: BaseModel | None = None) -> BaseModel:
        response = self.crud_requester.post(base_model)
        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url} and Validated Model"):
            allure.attach(f"Validated Model response: {self.endpoint.value.response_model.__name__}")
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate_json(response.text, by_alias=True)

    def delete(self, user_id: int):
        response = self.crud_requester.delete(user_id)
        return self.endpoint.value.response_model.model_validate_json(response.text, by_alias=True)
