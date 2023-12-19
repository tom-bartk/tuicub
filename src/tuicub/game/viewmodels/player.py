from attrs import frozen
from prompt_toolkit.formatted_text import StyleAndTextTuples

from ...common.models import Player
from ...common.strings import GAME_TILE_ICON_2
from ...common.views import Color, Theme


@frozen
class PlayerViewModel:
    """A viewmodel for a player widget.

    Attributes:
        player (Player): The player to display.
    """

    player: Player

    def content(self, theme: Theme) -> StyleAndTextTuples:
        """Returns the `prompt_toolkit` text content of the widget."""
        has_turn = self.player.has_turn
        background = Color.GREEN_DARK if has_turn else Color.BG7
        foreground = Color.FG0 if has_turn else Color.FG2
        separator_color = Color.GREEN if has_turn else Color.FG5
        return [
            (
                theme.style(fg=foreground, bg=background, bold=has_turn),
                f" {self.player.name} ",
            ),
            (theme.style(fg=separator_color, bg=background), "Ⅰ"),
            (
                theme.style(fg=foreground, bg=background),
                f"{GAME_TILE_ICON_2} {self.player.tiles_count} ",
            ),
        ]
