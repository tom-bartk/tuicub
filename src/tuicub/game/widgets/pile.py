from prompt_toolkit import formatted_text
from prompt_toolkit.layout.screen import Screen

from ...common.views import Theme
from ..viewmodels.pile import PileViewModel
from .base import BaseWidget
from .frame import Frame
from .renderer import Renderer

HEIGHT = 3
PADDING_RIGHT = 2


class PileWidget(BaseWidget):
    """A widget displaying the number of tiles on the pile."""

    __slots__ = ("_viewmodel", "_theme")

    @property
    def width(self) -> int:
        return (
            formatted_text.fragment_list_width(self._viewmodel.content(theme=self._theme))
            + PADDING_RIGHT
        )

    @property
    def height(self) -> int:
        return HEIGHT

    def __init__(self, viewmodel: PileViewModel, theme: Theme) -> None:
        self._viewmodel: PileViewModel = viewmodel
        self._theme: Theme = theme

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.write_content(self._viewmodel.content(theme=self._theme), frame, screen)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PileWidget):
            return NotImplemented

        return self._viewmodel == other._viewmodel
