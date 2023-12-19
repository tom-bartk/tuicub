import pytest

from src.tuicub.game.actions import UpdateBoardAction, UpdateBoardReducer
from src.tuicub.game.models import Board
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> UpdateBoardReducer:
    return UpdateBoardReducer()


class TestActionType:
    def test_returns_update_board_action(self, sut) -> None:
        expected = UpdateBoardAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_current_new_tiles_from_rack_added_to_new_tiles(
        self, sut, tile, tileset
    ) -> None:
        current = GameScreenState(
            board=Board(tilesets=frozenset({tileset(4, 5, 6)})),
            rack=tileset(1, 2, 3),
            new_tiles=frozenset({tile(3), tile(4), tile(5)}),
        )
        expected = GameScreenState(
            board=Board(tilesets=frozenset({tileset(4, 5, 6), tileset(7, 8, 9)})),
            rack=tileset(1, 2, 3),
            new_tiles=frozenset({tile(3), tile(7), tile(8), tile(9)}),
        )

        result = sut.apply(
            UpdateBoardAction(
                board=Board(tilesets=frozenset({tileset(4, 5, 6), tileset(7, 8, 9)})),
                new_tiles=frozenset({tile(7), tile(8), tile(9)}),
            ),
            state=current,
        )

        assert result == expected
