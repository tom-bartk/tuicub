from __future__ import annotations

from collections.abc import Callable, Sequence

from attrs import field, frozen
from prompt_toolkit.formatted_text import StyleAndTextTuples

from .color import Color, Theme

FLEX_SENTINEL = "[Flex]"


@frozen
class TextPart:
    text: str
    """The raw string representation."""

    fg: Color | None = field(default=None)
    """The optional foreground color."""

    bg: Color | None = field(default=None)
    """The optional background color."""

    bold: bool = field(default=False)
    """Is bold."""

    @classmethod
    def flex(cls) -> TextPart:
        return TextPart(text=FLEX_SENTINEL)


class Text:
    __slots__ = ("_parts",)

    @property
    def text(self) -> str:
        """The raw string representation."""
        return "".join(tuple(part.text for part in self._parts))

    @property
    def parts(self) -> Sequence[TextPart]:
        """The list of text parts composing this text."""
        return self._parts

    def __init__(self, *parts: TextPart):
        """Initialize new text.

        Args:
            parts (*TextPart): The parts of the text.
        """
        self._parts: Sequence[TextPart] = parts

    @classmethod
    def plain(cls, text: str, fg: Color | None = None, bold: bool = False) -> Text:
        """Initialize new plain text.

        Args:
            text (str): The string content.
            fg (Color): The color of the text.
            bold (bool): Should the text be bold.
        """
        return Text(TextPart(text=text, fg=fg, bold=bold))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Text):
            return NotImplemented

        return self.parts == other.parts

    def __hash__(self) -> int:
        return hash(self._parts)


def keybind(
    key: str, key_color: Color = Color.YELLOW, brackets_color: Color = Color.BG8
) -> tuple[TextPart, TextPart, TextPart]:
    return (
        TextPart("❬", fg=brackets_color),
        TextPart(key, fg=key_color, bold=True),
        TextPart("❭", fg=brackets_color),
    )


EMPTY_TEXT = Text()


AnyText = Text | Callable[[], Text] | str


class FrameworkText:
    __slots__ = ("_text", "_theme")

    def __init__(self, text: AnyText, theme: Theme):
        self._text: AnyText = text
        self._theme: Theme = theme

    def __pt_formatted_text__(self) -> StyleAndTextTuples:
        if isinstance(self._text, str):
            return [("", self._text)]
        text: Text = self._text() if callable(self._text) else self._text
        return [to_style_text_tuple(part, self._theme) for part in text.parts]


def to_style_text_tuple(part: TextPart, theme: Theme) -> tuple[str, str]:
    if part.text == "[Flex]":
        return "[Flex]", ""
    style = ""
    if part.fg:
        style += theme.to_framework_fg(part.fg)
    if part.bg:
        style += theme.to_framework_bg(part.bg)
    if part.bold:
        style += "bold"
    return style, part.text
