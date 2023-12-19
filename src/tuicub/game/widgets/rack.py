from prompt_toolkit.layout.screen import Screen

from ...common.views import Color, Theme
from ..consts import TILESET_HEIGHT
from ..viewmodels.tileset import TilesetViewModel
from .base import BaseWidget
from .frame import Frame
from .renderer import Position, Renderer, SeparatorSide, Side
from .tileset import TilesetWidget


class RackWidget(BaseWidget):
    """A widget displaying the current user's rack."""

    __slots__ = ("_tileset",)

    @property
    def height(self) -> int:
        return TILESET_HEIGHT

    def __init__(self, viewmodel: TilesetViewModel, theme: Theme) -> None:
        self._tileset: TilesetWidget = TilesetWidget(
            viewmodel=viewmodel, parent_background=Color.BG3, theme=theme
        )

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.render_widget(
            self._tileset,
            position=Position.CENTER,
            side=Side.CENTER,
            screen=screen,
            frame=frame,
        )
        renderer.draw_separator(SeparatorSide.TOP, frame, screen)
        renderer.set_background_color(Color.BG3, screen, frame)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RackWidget):
            return NotImplemented

        return self._tileset == other._tileset
