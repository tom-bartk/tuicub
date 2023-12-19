import pytest

from src.tuicub.game.actions import UpdatePlayersAction
from src.tuicub.game.events import PlayersChangedEvent, PlayersChangedEventHandler


@pytest.fixture()
def event(player_1, player_2, player_3) -> PlayersChangedEvent:
    return PlayersChangedEvent(players=[player_1, player_2, player_3])


@pytest.fixture()
def sut(store) -> PlayersChangedEventHandler:
    return PlayersChangedEventHandler(store=store)


class TestPlayersChangedEventHandler:
    def test_event_type__returns_players_changed_event(self, sut) -> None:
        expected = PlayersChangedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_update_players_action_with_players_from_event(
        self, sut, event, player_1, player_2, player_3
    ) -> None:
        expected = [UpdatePlayersAction(players=(player_1, player_2, player_3))]

        result = sut.actions(event=event)

        assert result == expected
