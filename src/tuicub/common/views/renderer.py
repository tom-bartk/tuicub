from prompt_toolkit.layout import Container
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.renderer import Screen, WritePosition


class Renderer:
    """A renderer that writes views on the screen."""

    __slots__ = ("_screen", "_parent_style", "_mouse_handlers")

    def __init__(self, screen: Screen, parent_style: str, mouse_handlers: MouseHandlers):
        """Initialize new renderer.

        Args:
            screen (Screen): The screen to write on.
            parent_style (str): The style string of the parent view.
            mouse_handlers (MouseHandlers): The mouse handlers.
        """
        self._screen: Screen = screen
        self._parent_style: str = parent_style
        self._mouse_handlers: MouseHandlers = mouse_handlers

    def render(
        self,
        container: Container,
        write_position: WritePosition,
        style: str | None = None,
    ) -> None:
        """Render the container at the given position.

        Args:
            container (Container): The container to render.
            write_position (WritePosition): The position to render at.
            style (str | None): An optional style to use.
        """
        container.write_to_screen(
            screen=self._screen,
            mouse_handlers=self._mouse_handlers,
            write_position=write_position,
            parent_style=style if style is not None else self._parent_style,
            erase_bg=False,
            z_index=None,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Renderer):
            return NotImplemented
        return (
            self._screen == other._screen
            and self._parent_style == other._parent_style
            and self._mouse_handlers == other._mouse_handlers
        )
