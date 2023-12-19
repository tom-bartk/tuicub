import pytest

from src.tuicub.game.actions import UpdatePlayersAction, UpdatePlayersReducer
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> UpdatePlayersReducer:
    return UpdatePlayersReducer()


class TestActionType:
    def test_returns_update_players_action(self, sut) -> None:
        expected = UpdatePlayersAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_pile_count(
        self, sut, player_1, player_2, player_3
    ) -> None:
        current = GameScreenState(players=(player_1, player_2, player_3))
        expected = GameScreenState(players=(player_1, player_2))

        result = sut.apply(
            UpdatePlayersAction(players=(player_1, player_2)), state=current
        )

        assert result == expected
