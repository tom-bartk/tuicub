import pytest

from src.tuicub.game.actions import (
    SetTilesetsSelectionAction,
    SetTilesetsSelectionReducer,
)
from src.tuicub.game.models import SelectionMode, Tileset
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> SetTilesetsSelectionReducer:
    return SetTilesetsSelectionReducer()


class TestActionType:
    def test_returns_set_tilesets_selection_action(self, sut) -> None:
        expected = SetTilesetsSelectionAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_tilesets_selection__virtual_tileset_from_selected_tiles(
        self, sut, virtual_tileset, tile
    ) -> None:
        current = GameScreenState(
            selection_mode=SelectionMode.TILES,
            highlighted_tileset=None,
            virtual_tileset=Tileset(),
            selected_tiles=frozenset({tile(1), tile(2), tile(3)}),
        )
        expected = GameScreenState(
            selection_mode=SelectionMode.TILESETS,
            highlighted_tileset=virtual_tileset(1, 2, 3),
            virtual_tileset=virtual_tileset(1, 2, 3),
            selected_tiles=frozenset({tile(1), tile(2), tile(3)}),
        )

        result = sut.apply(SetTilesetsSelectionAction(), state=current)

        assert result == expected
