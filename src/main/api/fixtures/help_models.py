from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse


class UserFixture(BaseModel):
    request: CreateUserRequest
    response: CreateUserResponse


class AccountFixture(BaseModel):
    user: UserFixture
    response: CreateAccountResponse
