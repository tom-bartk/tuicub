from prompt_toolkit.layout.screen import Screen

from ...common.views import Theme
from ..viewmodels.tileset import TilesetViewModel
from .base import BaseWidget, Frame
from .renderer import Renderer, VerticalPosition
from .row import RowWidget


class BoardWidget(BaseWidget):
    """The board widget displaying all played tilesets."""

    __slots__ = ("_rows",)

    def __init__(
        self, board: tuple[tuple[TilesetViewModel, ...], ...], theme: Theme
    ) -> None:
        self._rows: tuple[RowWidget, ...] = tuple(
            RowWidget(tilesets=tilesets, theme=theme) for tilesets in board
        )

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.render_vertically(
            self._rows, VerticalPosition.CENTER, frame, screen, width=frame.width
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BoardWidget):
            return NotImplemented

        return self._rows == other._rows
