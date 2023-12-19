import pytest

from src.tuicub.game.actions import AddDrawnTileAction, AddDrawnTileReducer
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> AddDrawnTileReducer:
    return AddDrawnTileReducer()


class TestActionType:
    def test_returns_add_drawn_tile_action(self, sut) -> None:
        expected = AddDrawnTileAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_tiles_as_single_set_with_drawn_tile(
        self, sut, tile
    ) -> None:
        expected = GameScreenState(new_tiles=frozenset({tile(42)}))

        result = sut.apply(AddDrawnTileAction(tile=tile(42)), state=GameScreenState())

        assert result == expected
