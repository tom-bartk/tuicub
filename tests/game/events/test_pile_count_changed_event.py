import pytest

from src.tuicub.game.actions import UpdatePileCountAction
from src.tuicub.game.events import PileCountChangedEvent, PileCountChangedEventHandler


@pytest.fixture()
def sut(store) -> PileCountChangedEventHandler:
    return PileCountChangedEventHandler(store=store)


class TestPileCountChangedEventHandler:
    def test_event_type__returns_board_changed_event(self, sut) -> None:
        expected = PileCountChangedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_update_pile_count_action_with_count_from_event(
        self, sut, tileset, tile
    ) -> None:
        event = PileCountChangedEvent(pile_count=42)
        expected = [UpdatePileCountAction(pile_count=42)]

        result = sut.actions(event=event)

        assert result == expected
