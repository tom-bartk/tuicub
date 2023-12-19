import pytest

from src.tuicub.game.actions import SetTilesSelectionAction, SetTilesSelectionReducer
from src.tuicub.game.models import SelectionMode, Tileset
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> SetTilesSelectionReducer:
    return SetTilesSelectionReducer()


class TestActionType:
    def test_returns_set_tiles_selection_action(self, sut) -> None:
        expected = SetTilesSelectionAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_tiles_selection_mode_and_empty_virtual_tileset(
        self, sut, virtual_tileset
    ) -> None:
        current = GameScreenState(
            selection_mode=SelectionMode.TILESETS,
            virtual_tileset=virtual_tileset(1, 2, 3),
        )
        expected = GameScreenState(
            selection_mode=SelectionMode.TILES, virtual_tileset=Tileset()
        )

        result = sut.apply(SetTilesSelectionAction(), state=current)

        assert result == expected
