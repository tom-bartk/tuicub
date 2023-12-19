from prompt_toolkit.formatted_text import to_formatted_text

from src.tuicub.common.views.color import Color
from src.tuicub.common.views.text import (
    FLEX_SENTINEL,
    FrameworkText,
    Text,
    TextPart,
    to_style_text_tuple,
)


class TestTextPart:
    def test_flex__returns_part_with_flex_sentinel(self) -> None:
        sut = TextPart.flex()

        assert sut.text == FLEX_SENTINEL


class TestText:
    def test_text__returns_combined_parts(self) -> None:
        parts = (
            TextPart("foo", fg=Color.FG1, bg=None, bold=True),
            TextPart("bar", fg=Color.FG2, bg=None, bold=False),
            TextPart("baz", fg=Color.FG3, bg=None, bold=True),
        )
        sut = Text(*parts)
        expected = "foobarbaz"

        result = sut.text

        assert result == expected

    def test_plain__returns_text_with_single_part(self) -> None:
        sut = Text.plain("foo", fg=Color.FG1, bold=True)
        expected = (TextPart("foo", fg=Color.FG1, bg=None, bold=True),)

        assert sut.parts == expected

    def test_hash__hashes_text_parts(self) -> None:
        parts = (
            TextPart("foo", fg=Color.FG1, bg=None, bold=True),
            TextPart("bar", fg=Color.FG2, bg=None, bold=False),
            TextPart("baz", fg=Color.FG3, bg=None, bold=True),
        )
        sut = Text(*parts)
        expected = hash(parts)

        result = hash(sut)

        assert result == expected


class TestFrameworkText:
    def test_pt_formatted_text__when_text_is_text_object__returns_style_and_text_tuples(
        self, theme
    ) -> None:
        sut = FrameworkText(text=Text.plain("foo"), theme=theme)
        expected = [("", "foo")]

        result = to_formatted_text(sut)

        assert result == expected

    def test_pt_formatted_text__when_text_is_string__returns_style_and_text_tuples(
        self, theme
    ) -> None:
        sut = FrameworkText(text="foo", theme=theme)
        expected = [("", "foo")]

        result = to_formatted_text(sut)

        assert result == expected

    def test_pt_formatted_text__when_text_is_callable__returns_style_and_text_tuples(
        self, theme
    ) -> None:
        sut = FrameworkText(text=lambda: Text.plain("foo"), theme=theme)
        expected = [("", "foo")]

        result = to_formatted_text(sut)

        assert result == expected


class TestToStyleTextTuple:
    def test_when_text_part_is_flex__returns_flex_style_with_empty_text(
        self, theme
    ) -> None:
        expected = (FLEX_SENTINEL, "")

        result = to_style_text_tuple(part=TextPart.flex(), theme=theme)

        assert result == expected

    def test_when_text_part_has_bg__adds_bg_to_style(self, theme) -> None:
        theme.to_framework_bg.return_value = "bg_color "
        expected = ("bg_color ", "foo")

        result = to_style_text_tuple(part=TextPart("foo", bg=Color.BG1), theme=theme)

        assert result == expected

    def test_when_text_part_has_fg__adds_fg_to_style(self, theme) -> None:
        theme.to_framework_fg.return_value = "fg_color "
        expected = ("fg_color ", "foo")

        result = to_style_text_tuple(part=TextPart("foo", fg=Color.FG1), theme=theme)

        assert result == expected

    def test_when_text_part_has_fg_and_bg__adds_fg_and_bg_to_style(self, theme) -> None:
        theme.to_framework_fg.return_value = "fg_color "
        theme.to_framework_bg.return_value = "bg_color "
        expected = ("fg_color bg_color ", "foo")

        result = to_style_text_tuple(
            part=TextPart("foo", fg=Color.FG1, bg=Color.BG1), theme=theme
        )

        assert result == expected

    def test_when_text_part_has_fg_and_bg_and_is_bold__adds_fg_and_bg_and_bold_to_style(
        self, theme
    ) -> None:
        theme.to_framework_fg.return_value = "fg_color "
        theme.to_framework_bg.return_value = "bg_color "
        expected = ("fg_color bg_color bold", "foo")

        result = to_style_text_tuple(
            part=TextPart("foo", fg=Color.FG1, bg=Color.BG1, bold=True), theme=theme
        )

        assert result == expected
