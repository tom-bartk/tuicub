import pytest

from src.tuicub.game.actions import StartTurnAction
from src.tuicub.game.events import TurnStartedEvent, TurnStartedEventHandler


@pytest.fixture()
def event() -> TurnStartedEvent:
    return TurnStartedEvent()


@pytest.fixture()
def sut(store) -> TurnStartedEventHandler:
    return TurnStartedEventHandler(store=store)


class TestTurnStartedEventHandler:
    def test_event_type__returns_turn_started_event(self, sut) -> None:
        expected = TurnStartedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_start_turn_action(self, sut, event) -> None:
        expected = [StartTurnAction()]

        result = sut.actions(event=event)

        assert result == expected
