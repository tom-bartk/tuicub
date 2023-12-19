from prompt_toolkit.formatted_text import to_plain_text

from src.tuicub.common.strings import (
    GAME_WINNER_PART_HAS_WON,
    GAME_WINNER_PART_PLAYER,
    GAME_WINNER_PART_WINNER,
)
from src.tuicub.game.viewmodels.winner import WinnerViewModel


class TestContent:
    def test_text_has_correct_text_with_winner_name(self, theme, player) -> None:
        sut = WinnerViewModel(winner=player)
        expected = (
            f"{GAME_WINNER_PART_WINNER}"
            f"{GAME_WINNER_PART_PLAYER}"
            f"{player.name}"
            f"{GAME_WINNER_PART_HAS_WON}"
        )
        result = to_plain_text(sut.content(theme=theme))

        assert result == expected
