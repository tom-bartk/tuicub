from unittest.mock import create_autospec

import pytest

from src.tuicub.app.actions import SetConfirmationAction, SetConfirmationReducer
from src.tuicub.app.state import AppState
from src.tuicub.common.confirmation import Confirmation


@pytest.fixture()
def sut() -> SetConfirmationReducer:
    return SetConfirmationReducer()


class TestActionType:
    def test_returns_set_confirmation_action(self, sut) -> None:
        expected = SetConfirmationAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_confirmation(self, sut) -> None:
        confirmation = create_autospec(Confirmation)
        current = AppState(confirmation=None)
        expected = AppState(confirmation=confirmation)

        result = sut.apply(SetConfirmationAction(confirmation), state=current)

        assert result == expected
