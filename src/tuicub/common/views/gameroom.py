import pendulum

from ..models import Gameroom, GameroomStatus
from ..strings import GAMEROOM_CREATED_AT_PREFIX, GAMEROOM_JUST_CREATED
from .color import Color
from .text import Text, TextPart

MAX_PLAYERS_COUNT = 4


def gameroom_text(
    gameroom: Gameroom, is_highlighted: bool = False, horizontal_padding: int = 2
) -> Text:
    """Returns an ui text content for a gameroom."""
    gray_shade = Color.BG6 if not is_highlighted else Color.BG8
    padding = horizontal_padding * " "
    players_count = len(gameroom.users)
    return Text(
        TextPart(f"\n{padding}{gameroom.name} ", Color.FG0),
        TextPart.flex(),
        TextPart("■" * players_count, squares_color(gameroom)),
        TextPart("□" * (MAX_PLAYERS_COUNT - players_count), gray_shade),
        TextPart(f" {players_count}/4", Color.FG3),
        separator(gameroom, gray_shade),
        badge(gameroom),
        TextPart(
            (
                f"{padding}\n{padding}"
                f"{GAMEROOM_CREATED_AT_PREFIX} {created_at_diff(gameroom)}."
            ),
            Color.FG4,
        ),
    )


def badge(gameroom: Gameroom) -> TextPart:
    fg = Color.GREEN_LIGHT
    bg = Color.GREEN_DIM
    if gameroom.status == GameroomStatus.RUNNING:
        fg = Color.YELLOW_LIGHT
        bg = Color.YELLOW_DIM
    elif gameroom.status == GameroomStatus.FINISHED:
        fg = Color.RED
        bg = Color.RED_DIM

    return TextPart(f" {gameroom.status} ", fg=fg, bg=bg, bold=True)


def separator(gameroom: Gameroom, fg: Color) -> TextPart:
    prefix = "  Ⅰ"
    text = (
        prefix.ljust(5)
        if not (
            gameroom.status == GameroomStatus.RUNNING
            or gameroom.status == GameroomStatus.DELETED
        )
        else prefix.ljust(6)
    )

    return TextPart(text, fg=fg)


def created_at_diff(gameroom: Gameroom) -> str:
    created_at = pendulum.instance(gameroom.created_at)
    minutes = created_at.diff().in_minutes()
    if minutes < 1:
        return GAMEROOM_JUST_CREATED

    return created_at.diff_for_humans()


def squares_color(gameroom: Gameroom) -> Color:
    free_spots = MAX_PLAYERS_COUNT - len(gameroom.users)
    match free_spots:
        case 3:
            return Color.GREEN_DARK
        case 2:
            return Color.YELLOW_DARK
        case 1:
            return Color.ORANGE_DARK
        case _:
            return Color.RED_DARK
