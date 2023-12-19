from unittest.mock import create_autospec

import pytest

from src.tuicub.common.models import Keybind
from src.tuicub.common.strings import REGISTER_USER_SUBMIT_KEY_TOOLTIP
from src.tuicub.register_user.controller import RegisterUserController
from src.tuicub.register_user.keybinds import RegisterUserKeybindsContainer


@pytest.fixture()
def controller() -> RegisterUserController:
    return create_autospec(RegisterUserController)


@pytest.fixture()
def sut(controller, app_store) -> RegisterUserKeybindsContainer:
    return RegisterUserKeybindsContainer(controller=controller, app_store=app_store)


class TestKeybinds:
    def test_contains_submit_keybind(self, sut, controller) -> None:
        expected = [
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=REGISTER_USER_SUBMIT_KEY_TOOLTIP,
                action=controller.register_user,
            )
        ]

        result = sut.keybinds()

        assert result == expected
