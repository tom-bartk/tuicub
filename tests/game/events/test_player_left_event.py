import pytest

from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.strings import GAME_PLAYER_LEFT_ALERT
from src.tuicub.game.events import PlayerLeftEvent, PlayerLeftEventHandler


@pytest.fixture()
def event(player) -> PlayerLeftEvent:
    return PlayerLeftEvent(player=player)


@pytest.fixture()
def sut(alert_service, store) -> PlayerLeftEventHandler:
    return PlayerLeftEventHandler(alert_service=alert_service, store=store)


class TestPlayerLeftEventHandler:
    def test_event_type__returns_player_left_event(self, sut) -> None:
        expected = PlayerLeftEvent

        result = sut.event_type

        assert result == expected

    def test_side_effects__queues_player_left_info_alert(
        self, sut, alert_service, event, player
    ) -> None:
        expected = Alert(GAME_PLAYER_LEFT_ALERT.format(player.name), AlertType.INFO)

        sut.side_effects(event=event)

        alert_service.queue_alert.assert_called_once_with(expected)
