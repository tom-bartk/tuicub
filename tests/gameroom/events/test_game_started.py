import pytest

from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.state import SetCurrentGameAction
from src.tuicub.common.strings import GAME_STARTED_ALERT
from src.tuicub.gameroom.events import GameStartedEvent, GameStartedEventHandler


@pytest.fixture()
def event(game) -> GameStartedEvent:
    return GameStartedEvent(game=game)


class TestGameStartedEventHandler:
    @pytest.fixture()
    def sut(self, alert_service, store) -> GameStartedEventHandler:
        return GameStartedEventHandler(alert_service=alert_service, store=store)

    def test_event_type__returns_game_started_event(
        self, sut: GameStartedEventHandler
    ) -> None:
        expected = GameStartedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_set_current_game_action_with_game_from_event(
        self, sut: GameStartedEventHandler, event, game
    ) -> None:
        expected = [SetCurrentGameAction(game=game)]

        result = sut.actions(event=event)

        assert result == expected

    def test_side_effects__queues_game_started_info_alert(
        self, sut: GameStartedEventHandler, alert_service, event
    ) -> None:
        expected = Alert(GAME_STARTED_ALERT, AlertType.INFO)

        sut.side_effects(event=event)

        alert_service.queue_alert.assert_called_once_with(expected)
