from __future__ import annotations

from collections.abc import Sequence
from enum import IntEnum
from typing import TYPE_CHECKING

from prompt_toolkit.formatted_text import (
    StyleAndTextTuples,
    fragment_list_width,
    split_lines,
)
from prompt_toolkit.layout.screen import _CHAR_CACHE, Screen

from ...common.strings import BOTTOM_BORDER, TOP_BORDER
from ...common.views import Color, Theme
from .frame import Frame

if TYPE_CHECKING:
    from .base import BaseWidget


class Renderer:
    """Renders game widgets on the screen."""

    __slots__ = ("_theme",)

    def __init__(self, theme: Theme):
        """Initialize new renderer.

        Args:
            theme (Theme): The theme to use.
        """
        self._theme: Theme = theme

    def write_content(
        self, content: StyleAndTextTuples, frame: Frame, screen: Screen
    ) -> None:
        """Write text content on the screen.

        Args:
            content (StyleAndTextTuples): The content to write.
            frame (Frame): The available frame.
            screen (Screen): The screen to write on.
        """
        for line_number, line in enumerate(split_lines(content)):
            self.draw_line(
                line=line, x_offset=0, y_offset=line_number, frame=frame, screen=screen
            )

    def write_centered_content(
        self, content: StyleAndTextTuples, frame: Frame, screen: Screen
    ) -> None:
        """Write centered text content on the screen.

        Args:
            content (StyleAndTextTuples): The content to write.
            frame (Frame): The available frame.
            screen (Screen): The screen to write on.
        """
        for line_number, line in enumerate(split_lines(content)):
            line_width = fragment_list_width(line)
            x = 0 if line_width >= frame.width else (frame.width - line_width) // 2
            self.draw_line(
                line=line, x_offset=x, y_offset=line_number, frame=frame, screen=screen
            )

    def draw_line(
        self,
        line: StyleAndTextTuples,
        x_offset: int,
        y_offset: int,
        frame: Frame,
        screen: Screen,
    ) -> None:
        """Write a single line of text on the screen.

        Args:
            line (StyleAndTextTuples): The line to write.
            x_offset (int): The offset on the x axis.
            y_offset (int): The offset on the y axis.
            frame (Frame): The available frame.
            screen (Screen): The screen to write on.
        """
        x = x_offset
        for style, text, *_ in line:
            for char in text:
                screen.data_buffer[frame.y + y_offset][x + frame.x] = _CHAR_CACHE[
                    char, style
                ]
                x += 1

    def draw_border(self, frame: Frame, screen: Screen, color: Color = Color.BG8) -> None:
        """Draws a border around the frame.

        Args:
            frame (Frame): The frame to draw border around.
            screen (Screen): The screen to write on.
            color (Color): The color of the border.
        """
        style = self._theme.to_framework_fg(color)

        top = frame.y
        bottom = frame.y + frame.height - 1
        left = frame.x
        right = frame.x + frame.width - 1

        # Draw corners
        screen.data_buffer[top][left] = _CHAR_CACHE["┏", style]
        screen.data_buffer[top][right] = _CHAR_CACHE["┓", style]
        screen.data_buffer[bottom][left] = _CHAR_CACHE["┗", style]
        screen.data_buffer[bottom][right] = _CHAR_CACHE["┛", style]

        # Draw vertical (left and right) borders
        for y in range(1, frame.height - 1):
            screen.data_buffer[frame.y + y][left] = _CHAR_CACHE["┃", style]
            screen.data_buffer[frame.y + y][right] = _CHAR_CACHE["┃", style]

        # Draw horizontal (top and bottom) borders
        for x in range(1, frame.width - 1):
            screen.data_buffer[top][frame.x + x] = _CHAR_CACHE["━", style]
            screen.data_buffer[bottom][frame.x + x] = _CHAR_CACHE["━", style]

    def draw_separator(
        self, side: SeparatorSide, frame: Frame, screen: Screen, color: Color = Color.BG5
    ) -> None:
        """Draws a separator line above or below the frame.

        Args:
            side (SeparatorSide): The side to write the separator on.
            frame (Frame): The frame to draw the separator for.
            screen (Screen): The screen to write on.
            color (Color): The color of the separator.
        """
        style = self._theme.to_framework_fg(color)

        if side == SeparatorSide.TOP:
            y = frame.y
            char = TOP_BORDER
        else:
            y = frame.y + frame.height - 1
            char = BOTTOM_BORDER

        for x in range(frame.width):
            screen.data_buffer[y][frame.x + x] = _CHAR_CACHE[char, style]

    def set_background_color(self, color: Color, screen: Screen, frame: Frame) -> None:
        """Sets the background color of the frame.

        Args:
            color (Color): The background color to set.
            screen (Screen): The screen to write on.
            frame (Frame): The frame to set the background color for.
        """
        screen.fill_area(
            frame.to_write_position(), style=self._theme.to_framework_bg(color)
        )

    def render_horizontally(
        self,
        widgets: Sequence[BaseWidget],
        position: HorizontalPosition,
        frame: Frame,
        screen: Screen,
        spacing: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
    ) -> None:
        """Render a list of widgets in a horizontal stack.

        Args:
            widgets (Sequence[BaseWidget]): The widgets to render.
            position (HorizontalPosition): The alignment of widgets along the x axis.
            frame (Frame): The available frame.
            screen (Screen): The screen to write on.
            spacing (int): The spacing between widgets.
            x_offset (int): The offset on the x axis.
            y_offset (int): The offset on the y axis.
        """
        match position:
            case HorizontalPosition.LEFT:
                x = frame.x + x_offset
                y = frame.y + y_offset
            case HorizontalPosition.CENTER:
                widgets_width = sum(tuple(widget.width + spacing for widget in widgets))
                x = frame.x + ((frame.width - widgets_width) // 2) + x_offset
                y = frame.y + y_offset

        for widget in widgets:
            widget.render(
                renderer=self,
                screen=screen,
                frame=Frame(x, y, widget.width, widget.height),
            )
            x += widget.width + spacing

    def render_vertically(
        self,
        widgets: Sequence[BaseWidget],
        position: VerticalPosition,
        frame: Frame,
        screen: Screen,
        width: int | None = None,
        spacing: int = 0,
        x_offset: int = 0,
        y_offset: int = 0,
    ) -> None:
        """Render a list of widgets in a vertical stack.

        Args:
            widgets (Sequence[BaseWidget]): The widgets to render.
            position (VerticalPosition): The alignment of widgets along the y axis.
            frame (Frame): The available frame.
            screen (Screen): The screen to write on.
            width: (int | None): The optional width to set for all widgets.
            spacing (int): The spacing between widgets.
            x_offset (int): The offset on the x axis.
            y_offset (int): The offset on the y axis.
        """
        match position:
            case VerticalPosition.TOP:
                x = frame.x + x_offset
                y = frame.y + y_offset
            case VerticalPosition.CENTER:
                widgets_height = sum(tuple(widget.height + spacing for widget in widgets))
                x = frame.x + x_offset
                y = frame.y + ((frame.height - widgets_height) // 2) + y_offset

        for widget in widgets:
            widget.render(
                renderer=self,
                screen=screen,
                frame=Frame(
                    x, y, width if width is not None else widget.width, widget.height
                ),
            )
            y += widget.height + spacing

    def render_widget(
        self,
        widget: BaseWidget,
        position: Position,
        side: Side,
        screen: Screen,
        frame: Frame,
        width: int | None = None,
        height: int | None = None,
        x_offset: int = 0,
        y_offset: int = 0,
    ) -> None:
        """Render a widget.

        Args:
            widget (BaseWidget): The widget to render.
            position (Position): The vertical position inside the frame.
            side (Side): The horizontal side inside the frame.
            frame (Frame): The available frame.
            screen (Screen): The screen to write on.
            width: (int | None): The optional width to set for the widget.
            height: (int | None): The optional height to set for the widget.
            x_offset (int): The offset on the x axis.
            y_offset (int): The offset on the y axis.
        """
        _width = width if width is not None else widget.width
        _height = height if height is not None else widget.height

        match side:
            case Side.LEFT:
                x = frame.x + x_offset
            case Side.RIGHT:
                x = frame.x + (frame.width - _width) - x_offset
            case Side.CENTER:
                x = frame.x + ((frame.width - _width) // 2) + x_offset

        match position:
            case Position.TOP:
                y = frame.y + y_offset
            case Position.BOTTOM:
                y = frame.y + (frame.height - _height) - y_offset
            case Position.CENTER:
                y = frame.y + ((frame.height - _height) // 2) + y_offset

        widget.render(renderer=self, screen=screen, frame=Frame(x, y, _width, _height))


class SeparatorSide(IntEnum):
    TOP = 1
    BOTTOM = 2


class HorizontalPosition(IntEnum):
    LEFT = 1
    CENTER = 2


class VerticalPosition(IntEnum):
    TOP = 1
    CENTER = 2


class Position(IntEnum):
    TOP = 1
    BOTTOM = 2
    CENTER = 3


class Side(IntEnum):
    LEFT = 1
    RIGHT = 2
    CENTER = 3
