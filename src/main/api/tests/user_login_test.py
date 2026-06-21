import pytest

from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_admin_request = LoginUserRequest(username="admin", password="123456")

        response = api_manager.admin_steps.login_user(login_admin_request)

        assert login_admin_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager, user_factory):
        user = user_factory()
        response = api_manager.admin_steps.login_user(user.request)

        assert user.response.username == response.user.username
        assert response.user.role == "ROLE_USER"
