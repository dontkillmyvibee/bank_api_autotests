from typing import Any

import pytest

from src.main.api.classes.api_manager import APIManager


@pytest.fixture
def api_manager(created_obj: list[Any]):
    return APIManager(created_obj)


