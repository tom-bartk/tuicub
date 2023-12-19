import pytest

from src.tuicub.common.state import FinishGameAction, FinishGameReducer, State


@pytest.fixture()
def sut() -> FinishGameReducer:
    return FinishGameReducer()


class TestActionType:
    def test_returns_finish_game_action(self, sut) -> None:
        expected = FinishGameAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_without_current_gameroom_and_current_game(
        self, sut, gameroom_1, gameroom_2, gameroom_3, game
    ) -> None:
        expected = State(
            current_gameroom=None, current_game=None, gamerooms=(gameroom_1, gameroom_2)
        )

        result = sut.apply(
            FinishGameAction(),
            state=State(
                current_gameroom=gameroom_3,
                current_game=game,
                gamerooms=(gameroom_1, gameroom_2, gameroom_3),
            ),
        )

        assert result == expected
