import pytest

from src.tuicub.game.actions import UpdateBoardAction
from src.tuicub.game.events import BoardChangedEvent, BoardChangedEventHandler
from src.tuicub.game.models import Board


@pytest.fixture()
def sut(store) -> BoardChangedEventHandler:
    return BoardChangedEventHandler(store=store)


class TestBoardChangedEventHandler:
    def test_event_type__returns_board_changed_event(self, sut) -> None:
        expected = BoardChangedEvent

        result = sut.event_type

        assert result == expected

    def test_actions__returns_update_board_action_with_board_from_event(
        self, sut, tileset, tile
    ) -> None:
        event = BoardChangedEvent(board=[[1, 2, 3], [4, 5, 6]], new_tiles=[1, 4])
        expected = [
            UpdateBoardAction(
                board=Board(tilesets=frozenset([tileset(1, 2, 3), tileset(4, 5, 6)])),
                new_tiles=frozenset([tile(1), tile(4)]),
            )
        ]

        result = sut.actions(event=event)

        assert result == expected
