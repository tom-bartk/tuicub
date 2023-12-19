from __future__ import annotations

from prompt_toolkit.layout import Window
from prompt_toolkit.layout.controls import FormattedTextControl


class FocusWindow(Window):
    """A dummy focusable window."""

    @property
    def control(self) -> FormattedTextControl:
        return self._control

    def __init__(self) -> None:
        self._control = FormattedTextControl(text="", focusable=True, show_cursor=False)
        super().__init__(
            self._control,
            width=1,
            height=1,
            always_hide_cursor=True,
            ignore_content_width=True,
            ignore_content_height=True,
            dont_extend_width=True,
            dont_extend_height=True,
        )
