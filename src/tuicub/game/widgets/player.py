from prompt_toolkit import formatted_text
from prompt_toolkit.layout.screen import Screen

from ...common.views import Theme
from ..viewmodels.player import PlayerViewModel
from .base import BaseWidget
from .frame import Frame
from .renderer import Renderer

HEIGHT = 1


class PlayerWidget(BaseWidget):
    """A widget displaying a single player."""

    __slots__ = ("_viewmodel", "_theme")

    @property
    def width(self) -> int:
        return formatted_text.fragment_list_width(
            self._viewmodel.content(theme=self._theme)
        )

    @property
    def height(self) -> int:
        return HEIGHT

    def __init__(self, viewmodel: PlayerViewModel, theme: Theme) -> None:
        self._viewmodel: PlayerViewModel = viewmodel
        self._theme: Theme = theme

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.write_content(self._viewmodel.content(theme=self._theme), frame, screen)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlayerWidget):
            return NotImplemented

        return self._viewmodel == other._viewmodel
