import pytest

from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.state import RemoveGameroomUserAction
from src.tuicub.common.strings import GAMEROOM_USER_LEFT_ALERT
from src.tuicub.gameroom.events import UserLeftEvent, UserLeftEventHandler


@pytest.fixture()
def event(user) -> UserLeftEvent:
    return UserLeftEvent(user=user)


class TestUserLeftEventHandler:
    @pytest.fixture()
    def sut(self, alert_service, store) -> UserLeftEventHandler:
        return UserLeftEventHandler(alert_service=alert_service, store=store)

    def test_event_type__returns_user_left_event(self, sut: UserLeftEventHandler) -> None:
        expected = UserLeftEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_remove_gameroom_user_action_with_user_from_event(
        self, sut: UserLeftEventHandler, event, user
    ) -> None:
        expected = [RemoveGameroomUserAction(user=user)]

        result = sut.actions(event=event)

        assert result == expected

    def test_side_effects__queues_user_left_info_alert(
        self, sut: UserLeftEventHandler, alert_service, event, user
    ) -> None:
        expected = Alert(GAMEROOM_USER_LEFT_ALERT.format(user.name), AlertType.INFO)

        sut.side_effects(event=event)

        alert_service.queue_alert.assert_called_once_with(expected)
