import pytest

from src.tuicub.game.actions import ResetStateAction, ResetStateReducer
from src.tuicub.game.models import Board, SelectionMode, Tileset
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> ResetStateReducer:
    return ResetStateReducer()


class TestActionType:
    def test_returns_reset_state_action(self, sut) -> None:
        expected = ResetStateAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_reset_properties(
        self, sut, tile, tileset, virtual_tileset
    ) -> None:
        current = GameScreenState(
            rack=tileset(1, 2, 3),
            highlighted_tile=tile(42),
            highlighted_tileset=tileset(1, 2, 3),
            selection_mode=SelectionMode.TILESETS,
            selected_tiles=frozenset({tile(2), tile(3)}),
            virtual_tileset=virtual_tileset(2, 3),
        )
        expected = GameScreenState(
            rack=tileset(1, 2, 3),
            highlighted_tile=tile(1),
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
        )

        result = sut.apply(ResetStateAction(), state=current)

        assert result == expected

    def test_when_rack_has_no_tiles__state_has_current_highlighted_tile(
        self, sut, tile, tileset, virtual_tileset
    ) -> None:
        current = GameScreenState(
            rack=tileset(),
            highlighted_tile=tile(42),
            highlighted_tileset=tileset(1, 2, 3),
            selection_mode=SelectionMode.TILESETS,
            selected_tiles=frozenset({tile(2), tile(3)}),
            virtual_tileset=virtual_tileset(2, 3),
        )
        expected = GameScreenState(
            rack=tileset(),
            highlighted_tile=tile(42),
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
        )

        result = sut.apply(ResetStateAction(), state=current)

        assert result == expected

    def test_when_rack_has_no_tiles__no_current__state_has_first_from_board_highlighted_tile(  # noqa: E501
        self, sut, tile, tileset, virtual_tileset
    ) -> None:
        current = GameScreenState(
            board=Board(tilesets=frozenset({tileset(13, 42)})),
            rack=tileset(),
            highlighted_tile=None,
            highlighted_tileset=tileset(1, 2, 3),
            selection_mode=SelectionMode.TILESETS,
            selected_tiles=frozenset({tile(2), tile(3)}),
            virtual_tileset=virtual_tileset(2, 3),
        )
        expected = GameScreenState(
            board=Board(tilesets=frozenset({tileset(13, 42)})),
            rack=tileset(),
            highlighted_tile=tile(13),
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
        )

        result = sut.apply(ResetStateAction(), state=current)

        assert result == expected

    def test_when_rack_has_no_tiles__no_current__empty_board__state_has_no_highlighted_tile(  # noqa: E501
        self, sut, tile, tileset, virtual_tileset
    ) -> None:
        current = GameScreenState(
            board=Board(),
            rack=tileset(),
            highlighted_tile=None,
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILESETS,
            selected_tiles=frozenset(),
            virtual_tileset=virtual_tileset(),
        )
        expected = GameScreenState(
            board=Board(),
            rack=tileset(),
            highlighted_tile=None,
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
        )

        result = sut.apply(ResetStateAction(), state=current)

        assert result == expected
