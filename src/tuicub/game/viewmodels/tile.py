from attrs import frozen
from prompt_toolkit.formatted_text import StyleAndTextTuples

from ...common.views import Color, Theme
from ..models import Tile


@frozen
class TileViewModel:
    """A viewmodel for a tile widget.

    Attributes:
        tile (Tile): The tile to display.
        is_selected (bool): Whether the tile is currently selected.
        is_highlighted (bool): Whether the tile is currently highlighted.
        is_new: (bool): Whether the tile has been played or drawn this turn.
    """

    tile: Tile
    is_selected: bool
    is_highlighted: bool
    is_new: bool

    def content(self, parent_background: Color, theme: Theme) -> StyleAndTextTuples:
        """Returns the `prompt_toolkit` text content of the widget."""
        bottom_background_color = (
            self.tile.color.ui_selected_color
            if (self.is_selected or self.is_new)
            else Color.TILE_BG
        )
        tile_bg = (
            Color.TILE_BG if not self.is_selected else self.tile.color.ui_selected_color
        )
        border_color = (
            parent_background if not self.is_highlighted else Color.TILE_SELECTED_BORDER
        )
        number_background = (
            Color.TILE_BG_LIGHT
            if not self.is_selected
            else self.tile.color.ui_selected_color
        )
        number_foreground = (
            self.tile.color.ui_color if not self.is_selected else Color.TILE_FG_SELECTED
        )

        number = str(self.tile.number).ljust(2) if not self.tile.is_joker() else "J "

        return [
            (theme.style(fg=tile_bg, bg=border_color), "▗▄▄▖\n"),
            (theme.style(fg=border_color, bg=tile_bg), "▌"),
            (theme.style(fg=number_foreground, bg=number_background, bold=True), number),
            (theme.style(fg=tile_bg, bg=border_color), "▌\n"),
            (theme.style(fg=bottom_background_color, bg=border_color), "▝▀▀▘"),
        ]


@frozen
class VirtualTileViewModel(TileViewModel):
    """A viewmodel for a virtual tile widget."""

    def content(self, parent_background: Color, theme: Theme) -> StyleAndTextTuples:
        """Returns the `prompt_toolkit` text content of the widget."""
        return [
            (theme.style(fg=Color.BG7, bg=parent_background), "▗▄▄▖\n"),
            (theme.style(fg=parent_background, bg=Color.BG7), "▌"),
            (theme.style(fg=Color.BG8, bg=Color.BG8), "  "),
            (theme.style(fg=Color.BG7, bg=parent_background), "▌\n"),
            (theme.style(fg=Color.BG7, bg=parent_background), "▝▀▀▘"),
        ]
