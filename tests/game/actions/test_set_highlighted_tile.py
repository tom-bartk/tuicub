import pytest

from src.tuicub.game.actions import SetHighlightedTileAction, SetHighlightedTileReducer
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def sut() -> SetHighlightedTileReducer:
    return SetHighlightedTileReducer()


class TestActionType:
    def test_returns_set_highlighted_tile_action(self, sut) -> None:
        expected = SetHighlightedTileAction

        result = sut.action_type

        assert result == expected


class TestApply:
    def test_returns_state_with_new_highlighted_tile(self, sut, tile) -> None:
        current = GameScreenState(highlighted_tile=tile(13))
        expected = GameScreenState(highlighted_tile=tile(42))

        result = sut.apply(SetHighlightedTileAction(tile=tile(42)), state=current)

        assert result == expected
