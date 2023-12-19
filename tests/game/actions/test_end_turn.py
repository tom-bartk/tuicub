import pytest

from src.tuicub.game.actions import EndTurnAction, EndTurnReducer
from src.tuicub.game.models import SelectionMode, Tileset
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> EndTurnReducer:
    return EndTurnReducer()


class TestActionType:
    def test_returns_end_turn_action(self, sut) -> None:
        expected = EndTurnAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_reset_properties(
        self, sut, tile, tileset, virtual_tileset
    ) -> None:
        current = GameScreenState(
            highlighted_tile=tile(42),
            highlighted_tileset=tileset(1, 2, 3),
            selection_mode=SelectionMode.TILESETS,
            selected_tiles=frozenset({tile(2), tile(3)}),
            virtual_tileset=virtual_tileset(2, 3),
        )
        expected = GameScreenState(
            highlighted_tile=None,
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
        )

        result = sut.apply(EndTurnAction(), state=current)

        assert result == expected
