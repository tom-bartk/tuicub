from prompt_toolkit.layout.screen import Screen

from ...common.views import Theme
from ..viewmodels.status_bar import StatusBarViewModel
from .base import BaseWidget, Frame
from .renderer import Renderer

HEIGHT = 1


class StatusBarWidget(BaseWidget):
    """A widget displaying the current selection mode and a turn status."""

    __slots__ = ("_viewmodel", "_theme")

    @property
    def height(self) -> int:
        return HEIGHT

    def __init__(self, viewmodel: StatusBarViewModel, theme: Theme):
        self._viewmodel: StatusBarViewModel = viewmodel
        self._theme: Theme = theme

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.write_content(self._viewmodel.content(theme=self._theme), frame, screen)
        renderer.set_background_color(self._viewmodel.bar_bg_color(), screen, frame)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StatusBarWidget):
            return NotImplemented

        return self._viewmodel == other._viewmodel
