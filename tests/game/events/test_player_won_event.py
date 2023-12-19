import pytest

from src.tuicub.game.actions import SetWinnerAction
from src.tuicub.game.events import PlayerWonEvent, PlayerWonEventHandler


@pytest.fixture()
def event(player) -> PlayerWonEvent:
    return PlayerWonEvent(winner=player)


@pytest.fixture()
def sut(store) -> PlayerWonEventHandler:
    return PlayerWonEventHandler(store=store)


class TestPlayerWonEventHandler:
    def test_event_type__returns_player_won_event(self, sut) -> None:
        expected = PlayerWonEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_set_winner_action_with_winner_from_event(
        self, sut, event, player
    ) -> None:
        expected = [SetWinnerAction(winner=player)]

        result = sut.actions(event=event)

        assert result == expected
