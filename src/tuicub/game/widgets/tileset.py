from collections.abc import Sequence

from prompt_toolkit.layout.screen import Screen

from ...common.views import Color, Theme
from ..consts import TILESET_HEIGHT
from ..viewmodels.tileset import TilesetViewModel
from .base import BaseWidget
from .frame import Frame
from .renderer import HorizontalPosition, Renderer
from .tile import TileWidget

HORIZONTAL_PADDING = 1
VERTICAL_PADDING = 1


class TilesetWidget(BaseWidget):
    """A widget displaying a tileset."""

    __slots__ = ("_viewmodel", "_tiles")

    @property
    def width(self) -> int:
        return self._viewmodel.width()

    @property
    def height(self) -> int:
        return TILESET_HEIGHT

    def __init__(
        self, viewmodel: TilesetViewModel, parent_background: Color, theme: Theme
    ) -> None:
        self._viewmodel: TilesetViewModel = viewmodel
        self._tiles: Sequence[TileWidget] = tuple(
            TileWidget(viewmodel=tile, parent_background=parent_background, theme=theme)
            for tile in viewmodel.tiles
        )

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        if self._viewmodel.is_highlighted:
            renderer.draw_border(frame, screen)

        renderer.render_horizontally(
            widgets=self._tiles,
            position=HorizontalPosition.LEFT,
            frame=frame,
            screen=screen,
            x_offset=HORIZONTAL_PADDING,
            y_offset=VERTICAL_PADDING,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TilesetWidget):
            return NotImplemented

        return self._viewmodel == other._viewmodel
