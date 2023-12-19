from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from enum import IntEnum, auto

from more_itertools import first
from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import Container, ScrollablePane
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.layout.screen import Screen, WritePosition

from .color import AnyBackgroundColor, Theme
from .stack import Padding, StackView
from .textview import TextView


class ListRow(TextView, ABC):
    """Base class for a list row."""

    @property
    @abstractmethod
    def is_highlighted(self) -> bool:
        """Returns true if the row is currently highlighted."""


class ScrollDirection(IntEnum):
    UP = auto()
    DOWN = auto()


class ListView(ScrollablePane):
    """A view that displays a scrollable list of rows."""

    @property
    def key_bindings(self) -> KeyBindingsBase | None:
        return self._container.key_bindings

    @key_bindings.setter
    def key_bindings(self, value: KeyBindingsBase | None) -> None:
        self._container.key_bindings = value

    @property
    def rows(self) -> Sequence[ListRow]:
        return self._get_rows()

    def __init__(
        self,
        get_rows: Callable[[], Sequence[ListRow]],
        header: Container,
        background_color: AnyBackgroundColor | None = None,
        key_bindings: KeyBindingsBase | None = None,
        theme: Theme | None = None,
        padding: Padding | None = None,
    ) -> None:
        self._get_rows = get_rows
        self._header: Container = header

        self._container = StackView(
            children=self.get_content,
            key_bindings=key_bindings,
            background_color=background_color,
            theme=theme,
            padding=padding,
        )

        super().__init__(
            content=self._container,
            keep_cursor_visible=False,
            keep_focused_window_visible=True,
            show_scrollbar=False,
            display_arrows=False,
        )

    def write_to_screen(
        self,
        screen: Screen,
        mouse_handlers: MouseHandlers,
        write_position: WritePosition,
        parent_style: str,
        erase_bg: bool,
        z_index: int | None,
    ) -> None:  # Slighlty modified library code # pragma: no cover
        virtual_width = write_position.width
        virtual_height = self.content.preferred_height(
            virtual_width, self.max_available_height
        ).preferred

        virtual_height = min(
            max(virtual_height, write_position.height), self.max_available_height
        )

        temp_screen = Screen()
        temp_screen.show_cursor = False

        self.content.write_to_screen(
            temp_screen,
            MouseHandlers(),
            WritePosition(xpos=0, ypos=0, width=virtual_width, height=virtual_height),
            parent_style,
            erase_bg,
            z_index,
        )

        highlighted_row = first(
            (row for row in self._get_rows() if row.is_highlighted), None
        )

        if highlighted_row and (
            visible_win_write_pos := (
                temp_screen.visible_windows_to_write_positions.get(highlighted_row, None)
            )
        ):
            if (
                first_row := first(self._get_rows(), None)
            ) and highlighted_row == first_row:
                visible_win_write_pos.ypos = 0
            self._make_window_visible(
                write_position.height, virtual_height, visible_win_write_pos, None
            )
        self._copy_over_screen(screen, temp_screen, write_position, virtual_width)

        screen.width = max(screen.width, write_position.xpos + virtual_width)
        screen.height = max(screen.height, write_position.ypos + write_position.height)

        self._copy_over_write_positions(screen, temp_screen, write_position)

    def get_content(self) -> Sequence[Container]:
        return (self._header, *self._get_rows())
