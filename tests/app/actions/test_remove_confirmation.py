from unittest.mock import create_autospec

import pytest

from src.tuicub.app.actions import RemoveConfirmationAction, RemoveConfirmationReducer
from src.tuicub.app.state import AppState
from src.tuicub.common.confirmation import Confirmation


@pytest.fixture()
def sut() -> RemoveConfirmationReducer:
    return RemoveConfirmationReducer()


class TestActionType:
    def test_returns_remove_confirmation_action(self, sut) -> None:
        expected = RemoveConfirmationAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_no_confirmation(self, sut) -> None:
        confirmation = create_autospec(Confirmation)
        current = AppState(confirmation=confirmation)
        expected = AppState(confirmation=None)

        result = sut.apply(RemoveConfirmationAction(result=False), state=current)

        assert result == expected
