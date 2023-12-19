import pytest

from src.tuicub.game.actions import UpdateRackAction
from src.tuicub.game.events import RackChangedEvent, RackChangedEventHandler


@pytest.fixture()
def event() -> RackChangedEvent:
    return RackChangedEvent(rack=[1, 2, 3])


@pytest.fixture()
def sut(store) -> RackChangedEventHandler:
    return RackChangedEventHandler(store=store)


class TestRackChangedEventHandler:
    def test_event_type__returns_rack_changed_event(self, sut) -> None:
        expected = RackChangedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_update_rack_action_with_rack_from_event(
        self, sut, event, tileset
    ) -> None:
        expected = [UpdateRackAction(rack=tileset(1, 2, 3))]

        result = sut.actions(event=event)

        assert result == expected
