from attrs import frozen
from prompt_toolkit.formatted_text import StyleAndTextTuples

from ...common.strings import GAME_TILE_ICON_2
from ...common.views import Color, Theme


@frozen
class PileViewModel:
    """A viewmodel for the pile count widget.

    Attributes:
        pile_count (int): The number of tiles left to draw from the pile.
    """

    pile_count: int

    def content(self, theme: Theme) -> StyleAndTextTuples:
        """Returns the `prompt_toolkit` text content of the widget."""
        return [
            (
                theme.style(fg=Color.FG1, bg=Color.BG7, bold=True),
                f"\n  {GAME_TILE_ICON_2} {str(self.pile_count).ljust(3)} ",
            ),
        ]
