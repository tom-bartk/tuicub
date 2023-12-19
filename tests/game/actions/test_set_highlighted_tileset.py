import pytest

from src.tuicub.game.actions import (
    SetHighlightedTilesetAction,
    SetHighlightedTilesetReducer,
)
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> SetHighlightedTilesetReducer:
    return SetHighlightedTilesetReducer()


class TestActionType:
    def test_returns_set_highlighted_tileset_action(self, sut) -> None:
        expected = SetHighlightedTilesetAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_highlighted_tileset(self, sut, tileset) -> None:
        current = GameScreenState(highlighted_tileset=tileset(1, 2, 3))
        expected = GameScreenState(highlighted_tileset=tileset(4, 5, 6))

        result = sut.apply(
            SetHighlightedTilesetAction(tileset=tileset(4, 5, 6)), state=current
        )

        assert result == expected
