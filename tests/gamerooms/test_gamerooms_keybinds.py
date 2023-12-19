from unittest.mock import create_autospec

import pytest

from src.tuicub.common.models import Keybind
from src.tuicub.common.strings import (
    ARROW_DOWN,
    ARROW_UP,
    GAMEROOMS_CREATE_GAMEROOM_KEY_TOOLTIP,
    GAMEROOMS_JOIN_GAMEROOM_KEY_TOOLTIP,
    GAMEROOMS_REFRESH_KEY_TOOLTIP,
)
from src.tuicub.gamerooms.controller import GameroomsController
from src.tuicub.gamerooms.keybinds import GameroomsKeybindsContainer


@pytest.fixture()
def controller() -> GameroomsController:
    return create_autospec(GameroomsController)


@pytest.fixture()
def sut(controller, app_store) -> GameroomsKeybindsContainer:
    return GameroomsKeybindsContainer(controller=controller, app_store=app_store)


class TestKeybinds:
    def test_returns_correct_keybinds(self, sut, controller) -> None:
        expected = [
            Keybind(
                key="j",
                display_key="j",
                tooltip=ARROW_DOWN,
                action=controller.scroll_gamerooms_down,
            ),
            Keybind(
                key="k",
                display_key="k",
                tooltip=ARROW_UP,
                action=controller.scroll_gamerooms_up,
            ),
            Keybind(
                key="c",
                display_key="c",
                tooltip=GAMEROOMS_CREATE_GAMEROOM_KEY_TOOLTIP,
                action=controller.create_gameroom,
            ),
            Keybind(
                key="r",
                display_key="r",
                tooltip=GAMEROOMS_REFRESH_KEY_TOOLTIP,
                action=controller.refresh_gamerooms,
            ),
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=GAMEROOMS_JOIN_GAMEROOM_KEY_TOOLTIP,
                action=controller.join_gameroom,
            ),
        ]

        result = sut.keybinds()

        assert result == expected
