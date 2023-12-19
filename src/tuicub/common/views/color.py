from __future__ import annotations

from collections.abc import Callable
from enum import StrEnum
from typing import Any, TypeGuard


class Color(StrEnum):
    """Names of all colors."""

    FG0 = "fg0"
    FG1 = "fg1"
    FG2 = "fg2"
    FG3 = "fg3"
    FG4 = "fg4"
    FG5 = "fg5"
    FG_BLACK = "fg_black"

    BG0 = "bg0"
    BG1 = "bg1"
    BG2 = "bg2"
    BG3 = "bg3"
    BG4 = "bg4"
    BG5 = "bg5"
    BG6 = "bg6"
    BG7 = "bg7"
    BG8 = "bg8"
    GRAY = "gray"

    BLUE = "blue"
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    ORANGE = "orange"
    AQUA = "aqua"
    PURPLE = "purple"

    RED_DARK = "red_dark"
    YELLOW_DARK = "yellow_dark"
    GREEN_DARK = "green_dark"
    ORANGE_DARK = "orange_dark"

    AQUA_DIM = "aqua_dim"
    BLUE_DIM = "blue_dim"
    RED_DIM = "red_dim"
    YELLOW_DIM = "yellow_dim"
    GREEN_DIM = "green_dim"
    PURPLE_DIM = "purple_dim"

    YELLOW_LIGHT = "yellow_light"
    GREEN_LIGHT = "green_light"

    TILE_FG_SELECTED = "tile_fg_selected"
    TILE_BG_LIGHT = "tile_bg_light"
    TILE_BG = "tile_bg"
    TILE_BLUE = "tile_blue"
    TILE_YELLOW = "tile_yellow"
    TILE_RED = "tile_red"
    TILE_BLACK = "tile_black"
    TILE_BLACK_SELECTED = "tile_black_selected"
    TILE_SELECTED_BORDER = "tile_selected_border"


class Theme:
    """A color theme for coloring the application views."""

    __slots__ = ("_colors_to_hex",)

    def to_framework_bg(self, color: Color) -> str:
        """Converts a color to its `prompt_toolkit` background hex representation."""
        bg_hex = self._colors_to_hex.get(color, None) or DEFAULT_COLORS_MAP[color]
        return f"bg:{bg_hex} "

    def to_framework_fg(self, color: Color) -> str:
        """Converts a color to its `prompt_toolkit` foreground hex representation."""
        fg_hex = self._colors_to_hex.get(color, None) or DEFAULT_COLORS_MAP[color]
        return f"fg:{fg_hex} "

    def style(self, fg: Color, bg: Color, bold: bool = False) -> str:
        """Return a full `prompt_toolkit` style string.

        Returns a string of foreground and background hex representations
        of the passed color names, and an optional bold flag.

        Args:
            fg (Color): The name of the foreground color.
            bg (Color): The name of the background color.
            bold (bool): Should the bold flag be included. Defaults to false.

        Returns:
            The `prompt_toolkit` style string.
        """
        bold_ = "" if not bold else "bold"
        fg_hex = self._colors_to_hex.get(fg, None) or DEFAULT_COLORS_MAP[fg]
        bg_hex = self._colors_to_hex.get(bg, None) or DEFAULT_COLORS_MAP[bg]
        return f"fg:{fg_hex} bg:{bg_hex} {bold_}"

    def __init__(self, colors_map: dict[Color, str] | None = None):
        """Initialize new theme.

        Args:
            colors_map (dict[Color, str] | None): Dictionary mapping color names
                to their hex values.
        """
        self._colors_to_hex: dict[Color, str] = colors_map or DEFAULT_COLORS_MAP

    @classmethod
    def default(cls) -> Theme:
        return Theme()


AnyBackgroundColor = Color | None | Callable[[], Color | None]


def to_framework_bg(
    color: AnyBackgroundColor | None, theme: Theme
) -> Callable[[], str] | str:
    if not color:
        return ""

    def wrapped() -> str:
        _color: Color | None = color() if callable(color) else color
        return theme.to_framework_bg(_color) if _color else ""

    return wrapped


def to_color(value: AnyBackgroundColor) -> Color | None:
    return value() if callable(value) else value


DEFAULT_COLORS_MAP = {
    Color.FG_BLACK: "#191b1c",
    Color.FG0: "#fbf1c7",
    Color.FG1: "#ebdbb2",
    Color.FG2: "#d5c4a1",
    Color.FG3: "#bdae93",
    Color.FG4: "#a89984",
    Color.FG5: "#857a6b",
    Color.BG0: "#191b1c",
    Color.BG1: "#1d2021",
    Color.BG2: "#232425",
    Color.BG3: "#282828",
    Color.BG4: "#2d2c2c",
    Color.BG5: "#32302f",
    Color.BG6: "#3c3836",
    Color.BG7: "#504945",
    Color.BG8: "#665c54",
    Color.GRAY: "#928374",
    Color.AQUA: "#8ec07c",
    Color.AQUA_DIM: "#343D34",
    Color.PURPLE: "#d3869b",
    Color.PURPLE_DIM: "#413339",
    Color.RED: "#fb4934",
    Color.RED_DARK: "#cc241d",
    Color.RED_DIM: "#462726",
    Color.BLUE: "#83a598",
    Color.BLUE_DIM: "#304142",
    Color.YELLOW: "#fabd2f",
    Color.YELLOW_LIGHT: "#FAC74D",
    Color.YELLOW_DARK: "#d79921",
    Color.YELLOW_DIM: "#67552A",
    Color.GREEN: "#b8bb26",
    Color.GREEN_LIGHT: "#C5C646",
    Color.GREEN_DARK: "#98971a",
    Color.GREEN_DIM: "#454528",
    Color.ORANGE: "#fe8109",
    Color.ORANGE_DARK: "#d65d0e",
    Color.TILE_FG_SELECTED: "#fbf1c7",
    Color.TILE_BG_LIGHT: "#EDE6CD",
    Color.TILE_BG: "#DDD1BA",
    Color.TILE_BLUE: "#00ABC8",
    Color.TILE_YELLOW: "#F39300",
    Color.TILE_RED: "#D6070F",
    Color.TILE_BLACK: "#0C0A05",
    Color.TILE_BLACK_SELECTED: "#747474",
    Color.TILE_SELECTED_BORDER: "#504945",
}


def is_colors_map(value: dict[str, Any]) -> TypeGuard[dict[Color, str]]:
    if all(key in list(Color) for key in value) and all(
        isinstance(val, str) for val in value.values()
    ):
        return True
    return False
