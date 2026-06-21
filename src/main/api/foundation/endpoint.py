from dataclasses import dataclass
from enum import Enum

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.deposit_response import DepositResponse
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.repay_request import RepayRequest
from src.main.api.models.repay_response import RepayResponse
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.models.transfer_response import TransferResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: type[BaseModel] | None
    response_model: type[BaseModel] | None


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        url="/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )
    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users",
        response_model=None,
        request_model=None
    )
    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        response_model=LoginUserResponse,
        url="/auth/token/login"
    )
    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        response_model=CreateAccountResponse,
        url="/account/create"
    )
    DEPOSIT = EndpointConfiguration(
        request_model=DepositRequest,
        response_model=DepositResponse,
        url="/account/deposit"
    )
    TRANSFER = EndpointConfiguration(
        request_model=TransferRequest,
        response_model=TransferResponse,
        url="/account/transfer"
    )
    CREDIT_REQUEST = EndpointConfiguration(
        request_model=CreditRequest,
        response_model=CreditResponse,
        url="/credit/request"
    )
    CREDIT_REPAY = EndpointConfiguration(
        request_model=RepayRequest,
        response_model=RepayResponse,
        url="/credit/repay"
    )
