from prompt_toolkit.layout.screen import Screen

from ...common.views import Color, Theme
from ..consts import TILE_HEIGHT, TILE_WIDTH
from ..viewmodels.tile import TileViewModel
from .base import BaseWidget
from .frame import Frame
from .renderer import Renderer


class TileWidget(BaseWidget):
    """A widget displaying a single game tile."""

    __slots__ = ("_viewmodel", "_parent_background", "_theme")

    @property
    def width(self) -> int:
        return TILE_WIDTH

    @property
    def height(self) -> int:
        return TILE_HEIGHT

    def __init__(
        self, viewmodel: TileViewModel, parent_background: Color, theme: Theme
    ) -> None:
        self._viewmodel: TileViewModel = viewmodel
        self._parent_background = parent_background
        self._theme: Theme = theme

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.write_content(
            self._viewmodel.content(
                parent_background=self._parent_background, theme=self._theme
            ),
            frame,
            screen,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TileWidget):
            return NotImplemented

        return self._viewmodel == other._viewmodel
