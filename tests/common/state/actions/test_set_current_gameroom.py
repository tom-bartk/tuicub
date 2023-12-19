import pytest

from src.tuicub.common.state import (
    SetCurrentGameroomAction,
    SetCurrentGameroomReducer,
    State,
)


@pytest.fixture()
def sut() -> SetCurrentGameroomReducer:
    return SetCurrentGameroomReducer()


class TestActionType:
    def test_returns_set_current_gameroom_action(self, sut) -> None:
        expected = SetCurrentGameroomAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_updated_current_gameroom(self, sut, gameroom) -> None:
        expected = State(current_gameroom=gameroom)

        result = sut.apply(
            SetCurrentGameroomAction(gameroom=gameroom),
            state=State(current_gameroom=None),
        )

        assert result == expected
