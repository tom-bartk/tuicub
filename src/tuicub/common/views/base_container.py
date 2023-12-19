from abc import ABC, abstractmethod

from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import Container, Dimension
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.renderer import Screen, WritePosition

from .color import AnyBackgroundColor, Theme, to_framework_bg
from .renderer import Renderer


class BaseContainer(Container, ABC):
    """Base class for a `prompt_toolkit` container."""

    def __init__(
        self,
        background_color: AnyBackgroundColor | None = None,
        theme: Theme | None = None,
        key_bindings: KeyBindingsBase | None = None,
    ) -> None:
        self.key_bindings: KeyBindingsBase | None = key_bindings
        self.style = to_framework_bg(background_color, theme or Theme.default())

    @abstractmethod
    def render(
        self, renderer: Renderer, write_position: WritePosition, parent_style: str
    ) -> None:
        """Render this container using the renderer at the given position.

        Args:
            renderer (Renderer): The renderer to use.
            write_position (WritePosition): The position to render at.
            parent_style (str): The style of the parent view.
        """

    def preferred_height(self, width: int, max_available_height: int) -> Dimension:
        return Dimension(preferred=max_available_height)

    def preferred_width(self, max_available_width: int) -> Dimension:
        return Dimension(preferred=max_available_width)

    def write_to_screen(
        self,
        screen: Screen,
        mouse_handlers: MouseHandlers,
        write_position: WritePosition,
        parent_style: str,
        erase_bg: bool,
        z_index: int | None,
    ) -> None:
        self.render(
            Renderer(
                screen=screen, parent_style=parent_style, mouse_handlers=mouse_handlers
            ),
            write_position=write_position,
            parent_style=parent_style,
        )

    def reset(self) -> None:  # pragma: no cover
        pass

    def get_children(self) -> list[Container]:
        return []

    def get_key_bindings(self) -> KeyBindingsBase | None:
        return self.key_bindings


class BasicContainer(Container):
    """A subclass of the `prompt_toolkit` container with a default implementation."""

    def preferred_height(self, width: int, max_available_height: int) -> Dimension:
        return Dimension()

    def preferred_width(self, max_available_width: int) -> Dimension:
        return Dimension()

    def reset(self) -> None:  # pragma: no cover
        pass

    def get_children(self) -> list[Container]:
        return []
