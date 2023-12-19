import pytest

from src.tuicub.common.state import (
    SetCurrentUserAction,
    SetCurrentUserReducer,
    State,
)


@pytest.fixture()
def sut() -> SetCurrentUserReducer:
    return SetCurrentUserReducer()


class TestActionType:
    def test_returns_set_current_user_action(self, sut) -> None:
        expected = SetCurrentUserAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_updated_current_user(self, sut, user) -> None:
        expected = State(current_user=user)

        result = sut.apply(
            SetCurrentUserAction(user=user), state=State(current_user=None)
        )

        assert result == expected
