import pytest

from src.tuicub.common.state import (
    RemoveCurrentGameroomAction,
    RemoveCurrentGameroomReducer,
    State,
)


@pytest.fixture()
def sut() -> RemoveCurrentGameroomReducer:
    return RemoveCurrentGameroomReducer()


class TestActionType:
    def test_returns_remove_current_gameroom_action(self, sut) -> None:
        expected = RemoveCurrentGameroomAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_without_current_gameroom(self, sut, gameroom_1) -> None:
        expected = State(current_gameroom=None)

        result = sut.apply(
            RemoveCurrentGameroomAction(), state=State(current_gameroom=gameroom_1)
        )

        assert result == expected
