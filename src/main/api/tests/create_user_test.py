import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import APIManager
from src.main.api.db.crud.user_crud import UserCrudDb
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(
            self,
            api_manager: APIManager,
            create_user_request: CreateUserRequest,
            db_session: Session
    ):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = UserCrudDb.get_user_by_username(db=db_session, username=create_user_request.username)
        assert user_from_db.username == create_user_request.username, "Созданного пользователя нет в базе"

    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!sw0rd"),
            ("ab", "Pas!sw0rd"),
            ("abv!", "Pas!sw0rd"),
            ("KIriii", "Pas!sw0rdд"),
            ("Maxxx3", "Pas!w0"),
            ("Maxx4", "pas!sw0rd"),
            ("Maxxx6", "PAS!SW0RD"),
            ("Maxxx7", "Pas!swsord"),
            ("Maxxx8", "Passsw0rd")
        ]

    )
    def test_create_user_invalid(self, username: str, password: str, api_manager: APIManager, db_session: Session):
        create_user_request = CreateUserRequest(
            username=username,
            password=password,
            role="ROLE_USER"
        )

        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = UserCrudDb.get_user_by_username(db=db_session, username=create_user_request.username)

        assert user_from_db is None, "Пользователь создан, ошибка"
