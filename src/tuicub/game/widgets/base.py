from __future__ import annotations

from abc import ABC, abstractmethod

from prompt_toolkit.layout.screen import Screen

from .frame import Frame
from .renderer import Renderer


class BaseWidget(ABC):
    """Base class for game widgets."""

    __slots__ = ()

    @property
    def width(self) -> int:
        """The width of the widget in characters."""
        return 0

    @property
    def height(self) -> int:
        """The height of the widget in characters."""
        return 0

    @abstractmethod
    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        """Render this widget using the renderer.

        Args:
            renderer (Renderer): The renderer to use.
            screen (Screen): The screen to render on.
            frame (Frame): The available frame.
        """
