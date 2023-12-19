import pytest

from src.tuicub.game.actions import ToggleTileSelectedAction, ToggleTileSelectedReducer
from src.tuicub.game.models import SelectionMode
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> ToggleTileSelectedReducer:
    return ToggleTileSelectedReducer()


class TestActionType:
    def test_returns_toggle_tile_selected_action(self, sut) -> None:
        expected = ToggleTileSelectedAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_when_no_highlighted_tile__does_nothing(self, sut, tile) -> None:
        current = GameScreenState(
            highlighted_tile=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset({tile(2), tile(3)}),
        )
        expected = GameScreenState(
            highlighted_tile=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset({tile(2), tile(3)}),
        )

        result = sut.apply(ToggleTileSelectedAction(), state=current)

        assert result == expected

    def test_when_highlighted_tile_in_selected_tiles__removes_highlighted_from_selected(
        self, sut, tile
    ) -> None:
        current = GameScreenState(
            highlighted_tile=tile(2),
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset({tile(1), tile(2), tile(3)}),
        )
        expected = GameScreenState(
            highlighted_tile=tile(2),
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset({tile(1), tile(3)}),
        )

        result = sut.apply(ToggleTileSelectedAction(), state=current)

        assert result == expected

    def test_when_highlighted_tile_not_in_selected_tiles__adds_highlighted_to_selected(
        self, sut, tile
    ) -> None:
        current = GameScreenState(
            highlighted_tile=tile(2),
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset({tile(1), tile(3)}),
        )
        expected = GameScreenState(
            highlighted_tile=tile(2),
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset({tile(1), tile(2), tile(3)}),
        )

        result = sut.apply(ToggleTileSelectedAction(), state=current)

        assert result == expected
