import pytest

from src.tuicub.game.actions import SetWinnerAction, SetWinnerReducer
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> SetWinnerReducer:
    return SetWinnerReducer()


class TestActionType:
    def test_returns_set_winner_action(self, sut) -> None:
        expected = SetWinnerAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_winner(self, sut, player) -> None:
        current = GameScreenState(winner=None)
        expected = GameScreenState(winner=player)

        result = sut.apply(SetWinnerAction(winner=player), state=current)

        assert result == expected
