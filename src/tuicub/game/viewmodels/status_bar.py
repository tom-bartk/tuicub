from attrs import frozen
from prompt_toolkit.formatted_text import StyleAndTextTuples

from ...common.strings import (
    GAME_STATUS_MOVE_MODE,
    GAME_STATUS_SELECT_MODE,
    GAME_STATUS_TURN_DONE,
)
from ...common.views import Color, Theme
from ..models import SelectionMode


@frozen
class StatusBarViewModel:
    """A viewmodel for the status bar widget.

    Attributes:
        selection_mode (SelectionMode): The current selection mode.
        has_turn (bool): True if the user currently has turn, false otherwise.
    """

    selection_mode: SelectionMode
    has_turn: bool

    def bar_bg_color(self) -> Color:
        """Returns a background color according to the selection mode and turn status."""
        if not self.has_turn:
            return Color.BG5
        else:
            match self.selection_mode:
                case SelectionMode.TILES:
                    return Color.AQUA_DIM
                case SelectionMode.TILESETS:
                    return Color.PURPLE_DIM

    def content(self, theme: Theme) -> StyleAndTextTuples:
        """Returns the `prompt_toolkit` text content of the widget."""
        text = GAME_STATUS_TURN_DONE
        text_bg_color = Color.GRAY
        text_fg_color = Color.BG5

        if self.has_turn:
            match self.selection_mode:
                case SelectionMode.TILES:
                    text = GAME_STATUS_SELECT_MODE
                    text_bg_color = Color.AQUA
                    text_fg_color = Color.FG_BLACK
                case SelectionMode.TILESETS:
                    text = GAME_STATUS_MOVE_MODE
                    text_bg_color = Color.PURPLE
                    text_fg_color = Color.FG_BLACK

        return [(theme.style(fg=text_fg_color, bg=text_bg_color, bold=True), f" {text} ")]
