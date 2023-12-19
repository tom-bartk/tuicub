import pytest

from src.tuicub.game.actions import StartTurnAction, StartTurnReducer
from src.tuicub.game.models import SelectionMode, Tileset
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> StartTurnReducer:
    return StartTurnReducer()


class TestActionType:
    def test_returns_start_turn_action(self, sut) -> None:
        expected = StartTurnAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_reset_properties_and_highlighted_tile_first_from_rack(
        self, sut, tile, tileset, virtual_tileset
    ) -> None:
        current = GameScreenState(
            rack=tileset(4, 5, 6),
            highlighted_tile=tile(42),
            highlighted_tileset=tileset(1, 2, 3),
            selection_mode=SelectionMode.TILESETS,
            selected_tiles=frozenset({tile(2), tile(3)}),
            virtual_tileset=virtual_tileset(2, 3),
        )
        expected = GameScreenState(
            rack=tileset(4, 5, 6),
            highlighted_tile=tile(4),
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
            new_tiles=frozenset(),
        )

        result = sut.apply(StartTurnAction(), state=current)

        assert result == expected
