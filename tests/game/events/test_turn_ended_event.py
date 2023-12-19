import pytest

from src.tuicub.game.actions import EndTurnAction
from src.tuicub.game.events import TurnEndedEvent, TurnEndedEventHandler


@pytest.fixture()
def event() -> TurnEndedEvent:
    return TurnEndedEvent()


@pytest.fixture()
def sut(store) -> TurnEndedEventHandler:
    return TurnEndedEventHandler(store=store)


class TestTurnEndedEventHandler:
    def test_event_type__returns_turn_ended_event(self, sut) -> None:
        expected = TurnEndedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_end_turn_action(self, sut, event) -> None:
        expected = [EndTurnAction()]

        result = sut.actions(event=event)

        assert result == expected
