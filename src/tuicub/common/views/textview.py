from __future__ import annotations

from prompt_toolkit.layout import AnyDimension, FormattedTextControl, WindowAlign

from .color import AnyBackgroundColor, Color, Theme, to_color, to_framework_bg
from .text import AnyText, FrameworkText, Text
from .window import TuicubWindow


class TextView(TuicubWindow):
    """A view that displays text content."""

    @property
    def text(self) -> AnyText:
        """The displayed text."""
        return self._text

    @text.setter
    def text(self, value: AnyText) -> None:
        self._text: AnyText = value
        self._content.text = FrameworkText(value, self._theme)

    @property
    def background_color(self) -> AnyBackgroundColor | None:
        return self._background_color

    @background_color.setter
    def background_color(self, value: AnyBackgroundColor | None) -> None:
        self._background_color: AnyBackgroundColor | None = value
        self.style = to_framework_bg(color=value, theme=self._theme)

    def __init__(
        self,
        text: AnyText,
        background_color: AnyBackgroundColor | None = None,
        align: WindowAlign | None = None,
        theme: Theme | None = None,
        height: AnyDimension | None = None,
    ):
        self._theme: Theme = theme or Theme.default()
        self._content: FormattedTextControl = FormattedTextControl(show_cursor=False)
        super().__init__(
            content=self._content,
            dont_extend_height=True,
            align=align or WindowAlign.LEFT,
            height=height,
        )
        self.text = text
        self.background_color = background_color

    @classmethod
    def plain(
        cls,
        text: str,
        color: Color | None = None,
        align: WindowAlign | None = None,
        bold: bool = False,
        theme: Theme | None = None,
        height: AnyDimension | None = None,
    ) -> TextView:
        return TextView(
            Text.plain(text, color, bold=bold), align=align, theme=theme, height=height
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextView):
            return NotImplemented

        return (
            self.text == other.text
            and to_color(self.background_color) == to_color(other.background_color)
            and self.align == other.align
        )

    def __hash__(self) -> int:
        return hash((self.text, self.background_color, self.align, self.height))
