from __future__ import annotations

from collections.abc import Callable

from prompt_toolkit.layout import Window

from .color import Color, Theme


class SeparatorView(Window):
    """A view that draws a single line for separating content."""

    def __init__(
        self, bold: bool = True, color: Color | None = None, theme: Theme | None = None
    ):
        theme_ = theme or Theme.default()
        style: Callable[[], str] | str = theme_.to_framework_fg(color or Color.BG6)
        char = "─"
        if bold:
            char = "━"

        super().__init__(
            char=char,
            height=1,
            dont_extend_width=False,
            dont_extend_height=True,
            always_hide_cursor=True,
            style=style,
        )
