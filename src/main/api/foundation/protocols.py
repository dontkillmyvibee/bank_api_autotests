from typing import Protocol

from src.main.api.fixtures.help_models import AccountFixture, UserFixture


class AccountFactory(Protocol):
    def __call__(self, user: UserFixture | None = None) -> AccountFixture: ...


class UserFactory(Protocol):
    def __call__(self) -> UserFixture: ...
