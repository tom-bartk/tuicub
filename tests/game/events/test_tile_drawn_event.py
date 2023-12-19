import pytest

from src.tuicub.game.actions import AddDrawnTileAction
from src.tuicub.game.events import TileDrawnEvent, TileDrawnEventHandler


@pytest.fixture()
def event() -> TileDrawnEvent:
    return TileDrawnEvent(tile=1)


@pytest.fixture()
def sut(store) -> TileDrawnEventHandler:
    return TileDrawnEventHandler(store=store)


class TestTileDrawnEventHandler:
    def test_event_type__returns_tile_drawn_event(self, sut) -> None:
        expected = TileDrawnEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_add_drawn_tile_action_with_tile_from_event(
        self, sut, event, tile
    ) -> None:
        expected = [AddDrawnTileAction(tile=tile(1))]

        result = sut.actions(event=event)

        assert result == expected
