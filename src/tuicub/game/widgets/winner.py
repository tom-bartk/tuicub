from __future__ import annotations

from prompt_toolkit import formatted_text
from prompt_toolkit.layout.screen import Screen

from ...common.views import Color, Theme
from ..viewmodels.winner import WinnerViewModel
from .base import BaseWidget
from .frame import Frame
from .renderer import Renderer

HORIZONTAL_PADDING = 4


class WinnerWidget(BaseWidget):
    """A widget displaying the winner of the game."""

    __slots__ = ("_viewmodel", "_theme")

    @property
    def height(self) -> int:
        return len(
            list(formatted_text.split_lines(self._viewmodel.content(theme=self._theme)))
        )

    @property
    def width(self) -> int:
        return formatted_text.fragment_list_width(
            max(
                formatted_text.split_lines(self._viewmodel.content(theme=self._theme)),
                key=formatted_text.fragment_list_width,
            )
        ) + (HORIZONTAL_PADDING * 2)

    def __init__(self, viewmodel: WinnerViewModel, theme: Theme) -> None:
        self._viewmodel: WinnerViewModel = viewmodel
        self._theme: Theme = theme

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.write_centered_content(
            self._viewmodel.content(theme=self._theme), frame, screen
        )
        renderer.set_background_color(Color.BG1, screen, frame)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WinnerWidget):
            return NotImplemented

        return self._viewmodel == other._viewmodel
