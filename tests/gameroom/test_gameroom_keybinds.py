from unittest.mock import create_autospec

import pytest

from src.tuicub.common.models import Keybind
from src.tuicub.common.state import State
from src.tuicub.common.strings import (
    GAMEROOM_DELETE_GAMEROOM_KEY_TOOLTIP,
    GAMEROOM_LEAVE_GAMEROOM_KEY_TOOLTIP,
    GAMEROOM_START_GAME_KEY_TOOLTIP,
)
from src.tuicub.gameroom.controller import GameroomController
from src.tuicub.gameroom.keybinds import GameroomKeybindsContainer


@pytest.fixture()
def controller() -> GameroomController:
    return create_autospec(GameroomController)


@pytest.fixture()
def sut(controller, store, app_store) -> GameroomKeybindsContainer:
    return GameroomKeybindsContainer(
        controller=controller, store=store, app_store=app_store
    )


class TestKeybinds:
    def test_returns_correct_keybinds(self, sut, controller) -> None:
        expected = [
            Keybind(
                key="d",
                display_key="d",
                tooltip=GAMEROOM_DELETE_GAMEROOM_KEY_TOOLTIP,
                action=controller.delete_gameroom,
            ),
            Keybind(
                key="l",
                display_key="l",
                tooltip=GAMEROOM_LEAVE_GAMEROOM_KEY_TOOLTIP,
                action=controller.leave_gameroom,
            ),
            Keybind(
                key="s",
                display_key="s",
                tooltip=GAMEROOM_START_GAME_KEY_TOOLTIP,
                action=controller.start_game,
            ),
        ]

        result = sut.keybinds()

        assert result == expected

    def test_delete_gameroom__when_user_owns_current_gameroom__condition_is_true(
        self, sut, controller, store, gameroom_1, user_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_1, current_user=user_1)
        expected = True
        keybind, _, _ = sut.keybinds()

        result = keybind.condition()

        assert keybind.action == controller.delete_gameroom
        assert result == expected

    def test_delete_gameroom__when_user_does_not_own_current_gameroom__condition_is_false(
        self, sut, controller, store, gameroom_2, user_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_2, current_user=user_1)
        expected = False
        keybind, _, _ = sut.keybinds()

        result = keybind.condition()

        assert keybind.action == controller.delete_gameroom
        assert result == expected

    def test_leave_gameroom__when_user_owns_current_gameroom__condition_is_false(
        self, sut, controller, store, gameroom_1, user_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_1, current_user=user_1)
        expected = False
        _, keybind, _ = sut.keybinds()

        result = keybind.condition()

        assert keybind.action == controller.leave_gameroom
        assert result == expected

    def test_leave_gameroom__when_user_does_not_own_current_gameroom__condition_is_true(
        self, sut, controller, store, gameroom_2, user_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_2, current_user=user_1)
        expected = True
        _, keybind, _ = sut.keybinds()

        result = keybind.condition()

        assert keybind.action == controller.leave_gameroom
        assert result == expected

    def test_start_game__when_user_owns_current_gameroom__condition_is_true(
        self, sut, controller, store, gameroom_1, user_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_1, current_user=user_1)
        expected = True
        _, _, keybind = sut.keybinds()

        result = keybind.condition()

        assert keybind.action == controller.start_game
        assert result == expected

    def test_start_game__when_user_does_not_own_current_gameroom__condition_is_false(
        self, sut, controller, store, gameroom_2, user_1
    ) -> None:
        store.state = State(current_gameroom=gameroom_2, current_user=user_1)
        expected = False
        _, _, keybind = sut.keybinds()

        result = keybind.condition()

        assert keybind.action == controller.start_game
        assert result == expected
