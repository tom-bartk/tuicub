from prompt_toolkit.layout.screen import Screen

from ...common.views import Color, Theme
from ..consts import TILESET_HEIGHT
from ..viewmodels.tileset import TilesetViewModel
from .base import BaseWidget
from .frame import Frame
from .renderer import HorizontalPosition, Renderer
from .tileset import TilesetWidget


class RowWidget(BaseWidget):
    """A widget displaying a list of tilesets for a single row."""

    __slots__ = ("_tilesets",)

    @property
    def height(self) -> int:
        return TILESET_HEIGHT

    def __init__(self, tilesets: tuple[TilesetViewModel, ...], theme: Theme) -> None:
        self._tilesets: tuple[TilesetWidget, ...] = tuple(
            TilesetWidget(viewmodel=tileset, parent_background=Color.BG2, theme=theme)
            for tileset in tilesets
        )

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.render_horizontally(
            self._tilesets, HorizontalPosition.CENTER, frame, screen
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RowWidget):
            return NotImplemented

        return self._tilesets == other._tilesets
