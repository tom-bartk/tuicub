import pytest

from src.tuicub.common.state import SetCurrentGameAction, SetCurrentGameReducer, State


@pytest.fixture()
def sut() -> SetCurrentGameReducer:
    return SetCurrentGameReducer()


class TestActionType:
    def test_returns_set_current_game_action(self, sut) -> None:
        expected = SetCurrentGameAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_updated_current_game(self, sut, game) -> None:
        expected = State(current_game=game)

        result = sut.apply(
            SetCurrentGameAction(game=game), state=State(current_game=None)
        )

        assert result == expected
