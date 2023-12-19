from __future__ import annotations

from collections.abc import Callable

from prompt_toolkit.data_structures import Point
from prompt_toolkit.formatted_text import (
    AnyFormattedText,
    StyleAndTextTuples,
    to_formatted_text,
)
from prompt_toolkit.formatted_text.utils import fragment_list_width
from prompt_toolkit.layout import Window, WindowAlign
from prompt_toolkit.layout.controls import UIContent
from prompt_toolkit.layout.screen import _CHAR_CACHE, Screen, WritePosition
from prompt_toolkit.layout.utils import explode_text_fragments
from prompt_toolkit.utils import get_cwidth


class TuicubWindow(Window):
    """A subclass of the `prompt_toolkit` window with minor changes."""

    def _copy_body(  # noqa: C901,PLR0915
        self,
        ui_content: UIContent,
        new_screen: Screen,
        write_position: WritePosition,
        move_x: int,
        width: int,
        vertical_scroll: int = 0,
        horizontal_scroll: int = 0,
        wrap_lines: bool = False,
        highlight_lines: bool = False,
        vertical_scroll_2: int = 0,
        always_hide_cursor: bool = False,
        has_focus: bool = False,
        align: WindowAlign = WindowAlign.LEFT,
        get_line_prefix: Callable[[int, int], AnyFormattedText] | None = None,
    ) -> tuple[
        dict[int, tuple[int, int]], dict[tuple[int, int], tuple[int, int]]
    ]:  # pragma: no cover
        xpos = write_position.xpos + move_x
        ypos = write_position.ypos
        line_count = ui_content.line_count
        new_buffer = new_screen.data_buffer
        empty_char = _CHAR_CACHE["", ""]

        # Map visible line number to (row, col) of input.
        # 'col' will always be zero if line wrapping is off.
        visible_line_to_row_col: dict[int, tuple[int, int]] = {}

        # Maps (row, col) from the input to (y, x) screen coordinates.
        rowcol_to_yx: dict[tuple[int, int], tuple[int, int]] = {}

        def copy_line(  # noqa: C901,PLR0912,PLR0915
            line: StyleAndTextTuples,
            lineno: int,
            x: int,
            y: int,
            is_input: bool = False,
        ) -> tuple[int, int]:
            if is_input:  # noqa: SIM108
                current_rowcol_to_yx = rowcol_to_yx
            else:
                current_rowcol_to_yx = {}  # Throwaway dictionary.

            # Draw line prefix.
            if is_input and get_line_prefix:
                prompt = to_formatted_text(get_line_prefix(lineno, 0))
                x, y = copy_line(prompt, lineno, x, y, is_input=False)

            # Scroll horizontally.
            skipped = 0  # Characters skipped because of horizontal scrolling.
            if horizontal_scroll and is_input:
                h_scroll = horizontal_scroll
                line = explode_text_fragments(line)
                while h_scroll > 0 and line:
                    h_scroll -= get_cwidth(line[0][1])
                    skipped += 1
                    del line[:1]  # Remove first character.

                x -= h_scroll  # When scrolling over double width character,
                # this can end up being negative.

            # Align this line. (Note that this doesn't work well when we use
            # get_line_prefix and that function returns variable width prefixes.)
            if align == WindowAlign.CENTER:
                line_width = fragment_list_width(line)
                if line_width < width:
                    x += (width - line_width) // 2
            elif align == WindowAlign.RIGHT:
                line_width = fragment_list_width(line)
                if line_width < width:
                    x += width - line_width

            col = 0
            wrap_count = 0
            for style, text, *_ in line:
                new_buffer_row = new_buffer[y + ypos]

                # Remember raw VT escape sequences. (E.g. FinalTerm's
                # escape sequences.)
                if "[ZeroWidthEscape]" in style:
                    new_screen.zero_width_escapes[y + ypos][x + xpos] += text
                    continue
                # -----Modified part-----------------------------------------------
                _text = text
                if "[Flex]" in style:
                    remaining = width - fragment_list_width(line)
                    if remaining <= 0:
                        continue
                    _text = remaining * " "
                for c in _text:
                    # -Modified part end------------------------------------------
                    char = _CHAR_CACHE[c, style]
                    char_width = char.width

                    # Wrap when the line width is exceeded.
                    if wrap_lines and x + char_width > width:
                        visible_line_to_row_col[y + 1] = (
                            lineno,
                            visible_line_to_row_col[y][1] + x,
                        )
                        y += 1
                        wrap_count += 1
                        x = 0

                        # Insert line prefix (continuation prompt).
                        if is_input and get_line_prefix:
                            prompt = to_formatted_text(
                                get_line_prefix(lineno, wrap_count)
                            )
                            x, y = copy_line(prompt, lineno, x, y, is_input=False)

                        new_buffer_row = new_buffer[y + ypos]

                        if y >= write_position.height:
                            return x, y  # Break out of all for loops.

                    # Set character in screen and shift 'x'.
                    if x >= 0 and y >= 0 and x < width:
                        new_buffer_row[x + xpos] = char

                        # When we print a multi width character, make sure
                        # to erase the neighbours positions in the screen.
                        # (The empty string if different from everything,
                        # so next redraw this cell will repaint anyway.)
                        if char_width > 1:
                            for i in range(1, char_width):
                                new_buffer_row[x + xpos + i] = empty_char

                        # If this is a zero width characters, then it's
                        # probably part of a decomposed unicode character.
                        # See: https://en.wikipedia.org/wiki/Unicode_equivalence
                        # Merge it in the previous cell.
                        elif char_width == 0:
                            # Handle all character widths. If the previous
                            # character is a multiwidth character, then
                            # merge it two positions back.
                            for pw in [2, 1]:  # Previous character width.
                                if (
                                    x - pw >= 0
                                    and new_buffer_row[x + xpos - pw].width == pw
                                ):
                                    prev_char = new_buffer_row[x + xpos - pw]
                                    char2 = _CHAR_CACHE[
                                        prev_char.char + c, prev_char.style
                                    ]
                                    new_buffer_row[x + xpos - pw] = char2

                        # Keep track of write position for each character.
                        current_rowcol_to_yx[lineno, col + skipped] = (
                            y + ypos,
                            x + xpos,
                        )

                    col += 1
                    x += char_width
            return x, y

        # Copy content.
        def copy() -> int:
            y = -vertical_scroll_2
            lineno = vertical_scroll

            while y < write_position.height and lineno < line_count:
                # Take the next line and copy it in the real screen.
                line = ui_content.get_line(lineno)

                visible_line_to_row_col[y] = (lineno, horizontal_scroll)

                # Copy margin and actual line.
                x = 0
                x, y = copy_line(line, lineno, x, y, is_input=True)

                lineno += 1
                y += 1
            return y

        copy()

        def cursor_pos_to_screen_pos(row: int, col: int) -> Point:
            try:
                y, x = rowcol_to_yx[row, col]
            except KeyError:
                # Normally this should never happen. (It is a bug, if it happens.)
                # But to be sure, return (0, 0)
                return Point(x=0, y=0)

                # raise ValueError(
                #     'Invalid position. row=%r col=%r, vertical_scroll=%r, '
                #     'horizontal_scroll=%r, height=%r' %
                #     (row, col, vertical_scroll, horizontal_scroll, write_position.height))  # noqa: E501
            else:
                return Point(x=x, y=y)

        # Set cursor and menu positions.
        if ui_content.cursor_position:
            screen_cursor_position = cursor_pos_to_screen_pos(
                ui_content.cursor_position.y, ui_content.cursor_position.x
            )

            if has_focus:
                new_screen.set_cursor_position(self, screen_cursor_position)

                if always_hide_cursor:
                    new_screen.show_cursor = False
                else:
                    new_screen.show_cursor = ui_content.show_cursor

                self._highlight_digraph(new_screen)

            if highlight_lines:
                self._highlight_cursorlines(
                    new_screen,
                    screen_cursor_position,
                    xpos,
                    ypos,
                    width,
                    write_position.height,
                )

        # Draw input characters from the input processor queue.
        if has_focus and ui_content.cursor_position:
            self._show_key_processor_key_buffer(new_screen)

        # Set menu position.
        if ui_content.menu_position:
            new_screen.set_menu_position(
                self,
                cursor_pos_to_screen_pos(
                    ui_content.menu_position.y, ui_content.menu_position.x
                ),
            )

        # Update output screen height.
        new_screen.height = max(new_screen.height, ypos + write_position.height)

        return visible_line_to_row_col, rowcol_to_yx
