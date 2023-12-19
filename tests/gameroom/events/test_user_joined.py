import pytest

from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.state import AddGameroomUserAction
from src.tuicub.common.strings import GAMEROOM_USER_JOINED_ALERT
from src.tuicub.gameroom.events import UserJoinedEvent, UserJoinedEventHandler


@pytest.fixture()
def event(user) -> UserJoinedEvent:
    return UserJoinedEvent(user=user)


class TestUserJoinedEventHandler:
    @pytest.fixture()
    def sut(self, alert_service, store) -> UserJoinedEventHandler:
        return UserJoinedEventHandler(alert_service=alert_service, store=store)

    def test_event_type__returns_user_joined_event(
        self, sut: UserJoinedEventHandler
    ) -> None:
        expected = UserJoinedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_add_gameroom_user_action_with_user_from_event(
        self, sut: UserJoinedEventHandler, event, user
    ) -> None:
        expected = [AddGameroomUserAction(user=user)]

        result = sut.actions(event=event)

        assert result == expected

    def test_side_effects__queues_user_joined_info_alert(
        self, sut: UserJoinedEventHandler, alert_service, event, user
    ) -> None:
        expected = Alert(GAMEROOM_USER_JOINED_ALERT.format(user.name), AlertType.INFO)

        sut.side_effects(event=event)

        alert_service.queue_alert.assert_called_once_with(expected)
