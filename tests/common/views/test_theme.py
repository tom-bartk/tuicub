import pytest

from src.tuicub.common.views.color import Color, Theme, is_colors_map, to_framework_bg


@pytest.fixture()
def sut() -> Theme:
    return Theme()


class TestTheme:
    def test_style__when_not_bold__returns_framework_style_string(self, sut) -> None:
        expected = "fg:#ebdbb2 bg:#282828 "

        result = sut.style(fg=Color.FG1, bg=Color.BG3, bold=False)

        assert result == expected

    def test_style__when_bold__returns_framework_style_string_with_bold(
        self, sut
    ) -> None:
        expected = "fg:#ebdbb2 bg:#282828 bold"

        result = sut.style(fg=Color.FG1, bg=Color.BG3, bold=True)

        assert result == expected


class TestToFrameworkBg:
    def test_when_color_none__returns_empty_string(self, theme) -> None:
        expected = ""

        result = to_framework_bg(color=None, theme=theme)

        assert result == expected

    def test_when_color_callable__result_callable_returns_framwork_bg(
        self, theme
    ) -> None:
        def color() -> Color:
            return Color.BG3

        expected = "bg:#282828"
        theme.to_framework_bg.return_value = "bg:#282828"

        result = to_framework_bg(color=color, theme=theme)()  # type: ignore

        assert result == expected

    def test_when_color_not_callable__result_callable_returns_framwork_bg(
        self, theme
    ) -> None:
        color = Color.BG3
        expected = "bg:#282828"
        theme.to_framework_bg.return_value = "bg:#282828"

        result = to_framework_bg(color=color, theme=theme)()  # type: ignore

        assert result == expected


class TestIsColorsMap:
    def test_when_all_keys_colors__values_all_strings__returns_true(self) -> None:
        expected = True

        result = is_colors_map(value={Color.RED: "foo", Color.BLUE: "bar"})

        assert result == expected

    def test_when_all_keys_colors__values_not_all_strings__returns_false(self) -> None:
        expected = False

        result = is_colors_map(value={Color.RED: "foo", Color.BLUE: 42})

        assert result == expected

    def test_when_not_all_keys_colors__values_all_strings__returns_false(self) -> None:
        expected = False

        result = is_colors_map(value={Color.RED: "foo", "bar": "baz"})

        assert result == expected
