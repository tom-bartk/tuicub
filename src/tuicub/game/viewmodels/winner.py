from attrs import frozen
from prompt_toolkit.formatted_text import StyleAndTextTuples

from ...common.models import Player
from ...common.strings import (
    GAME_WINNER_PART_HAS_WON,
    GAME_WINNER_PART_PLAYER,
    GAME_WINNER_PART_WINNER,
)
from ...common.views import Color, Theme


@frozen
class WinnerViewModel:
    """A viewmodel for a winner widget.

    Attributes:
        winner (Player): The winner of the game.
    """

    winner: Player

    def content(self, theme: Theme) -> StyleAndTextTuples:
        """Returns the `prompt_toolkit` text content of the widget."""
        return [
            (f"{theme.to_framework_fg(Color.FG0)} bold", GAME_WINNER_PART_WINNER),
            (theme.to_framework_fg(Color.FG2), GAME_WINNER_PART_PLAYER),
            (f"{theme.to_framework_fg(Color.YELLOW)} bold", self.winner.name),
            (theme.to_framework_fg(Color.FG1), GAME_WINNER_PART_HAS_WON),
        ]
