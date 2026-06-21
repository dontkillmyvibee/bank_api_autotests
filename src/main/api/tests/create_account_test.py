from typing import Callable

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import APIManager
from src.main.api.db.crud.account_crud import AccountCrudDb


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, db_session: Session, api_manager: APIManager, user_factory: Callable):
        response = api_manager.user_steps.create_account(user_factory().request)

        assert response.balance == 0

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)

        assert account_from_db.id == response.id, "Аккаунт не создан, id аккаунта нет в бд"
        assert account_from_db.balance is not None, "Поле баланса для созданного аккаунта отсутствует в БД"
