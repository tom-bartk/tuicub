import pytest

from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.state import DeleteGameroomAction
from src.tuicub.common.strings import GAMEROOM_DELETED_ALERT
from src.tuicub.gameroom.events import GameroomDeletedEvent, GameroomDeletedEventHandler


@pytest.fixture()
def event(gameroom) -> GameroomDeletedEvent:
    return GameroomDeletedEvent(gameroom=gameroom)


class TestGameroomDeletedEventHandler:
    @pytest.fixture()
    def sut(self, alert_service, store) -> GameroomDeletedEventHandler:
        return GameroomDeletedEventHandler(alert_service=alert_service, store=store)

    def test_event_type__returns_gameroom_deleted_event(
        self, sut: GameroomDeletedEventHandler
    ) -> None:
        expected = GameroomDeletedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_delete_gameroom_action_with_gameroom_from_event(
        self, sut: GameroomDeletedEventHandler, event, gameroom
    ) -> None:
        expected = [DeleteGameroomAction(gameroom=gameroom)]

        result = sut.actions(event=event)

        assert result == expected

    def test_side_effects__queues_gameroom_deleted_info_alert(
        self, sut: GameroomDeletedEventHandler, alert_service, event
    ) -> None:
        expected = Alert(GAMEROOM_DELETED_ALERT, AlertType.INFO)

        sut.side_effects(event=event)

        alert_service.queue_alert.assert_called_once_with(expected)
