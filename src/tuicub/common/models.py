from __future__ import annotations

from collections.abc import Awaitable, Callable, Generator
from datetime import datetime
from enum import IntEnum, StrEnum
from typing import NamedTuple

from attrs import field, frozen
from more_itertools import first
from prompt_toolkit.filters import Condition as PtCondition
from prompt_toolkit.filters import Filter
from prompt_toolkit.filters.app import buffer_has_focus
from prompt_toolkit.key_binding import KeyPressEvent

from .views import Color, Text, TextPart
from .views.animation import TextAnimation
from .views.text import EMPTY_TEXT


@frozen
class User:
    """An end user of the application.

    Attributes:
        id (str): The unique identifier of the user.
        name (str): The chosen nickname of the user.
    """

    id: str
    name: str


@frozen
class Gameroom:
    """A model representing a gameroom.

    Attributes:
        id (str): The id of the gameroom.
        name (str): The name of the gameroom.
        owner_id (str): The id of the user that the gameroom belongs to.
        status (GameroomStatus): The status of the gameroom.
        users (tuple[User, ...]): Users that joined this gameroom, including the owner.
        game_id (str | None): An optional id of the game started in this gameroom.
        created_at (datetime): The gameroom's date of creation.
    """

    id: str
    name: str
    owner_id: str
    status: GameroomStatus
    users: tuple[User, ...]
    game_id: str | None
    created_at: datetime = field(default=datetime.now(), eq=False)


@frozen
class Game:
    """A model representing a game.

    Attributes:
        id (str): The id of the game.
        gameroom_id (str): The id of the gameroom that the game belongs to.
        game_state (GameState): The current state of the game.
        winner (Player | None): An optional winner of the game.
    """

    id: str
    gameroom_id: str
    game_state: GameState
    winner: Player | None = field(default=None)


@frozen
class GameState:
    """A model representing a state of a game.

    Attributes:
        players (list[Player]): Players participating in this game.
        board (list[list[int]]): The current board of the game.
        pile_count (int): The current number of tiles on the pile.
        rack (list[int]): The current rack of the user.
    """

    players: list[Player]
    board: list[list[int]]
    pile_count: int
    rack: list[int]

    def __attrs_post_init__(self):
        object.__setattr__(self, "rack", sorted_tileset(self.rack))


@frozen
class Player:
    """A player representing a user in a game.

    Attributes:
        user_id (str): The id of the user that this player represents.
        name (str): The name of the player.
        tiles_count (int): The current number of tiles in the player's rack.
        has_turn (bool): Whether the player currently has a turn.
    """

    user_id: str
    name: str
    tiles_count: int
    has_turn: bool


class GameroomStatus(StrEnum):
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    DELETED = "DELETED"


class AlertType(IntEnum):
    ERROR = 1
    INFO = 2
    SUCCESS = 3
    WARNING = 4

    @property
    def color(self) -> Color:
        match self:
            case AlertType.SUCCESS:
                return Color.GREEN_LIGHT
            case AlertType.INFO:
                return Color.BLUE
            case AlertType.ERROR:
                return Color.RED
            case AlertType.WARNING:
                return Color.ORANGE

    @property
    def animation_duration(self) -> int:
        if self == AlertType.INFO:
            return 5
        return 3

    @property
    def animation_fps(self) -> int:
        if self == AlertType.INFO:
            return 2
        return 4


@frozen
class Alert:
    """The alert to display on the status bar."""

    text: str
    type_: AlertType

    @property
    def text_part(self) -> TextPart:
        match self.type_:
            case AlertType.SUCCESS:
                symbol = " ✔"
            case AlertType.INFO:
                symbol = " ℹ"
            case AlertType.ERROR | AlertType.WARNING:
                symbol = " ⚠ "
        return TextPart(f"{symbol} {self.text} ", fg=self.type_.color)

    @property
    def animation_frames(self) -> Generator[Text, None, None]:
        """Returns a generator producing text frames to animate."""
        seconds = self.type_.animation_duration
        fps = self.type_.animation_fps
        for i in range(seconds * fps + 1):
            yield Text(
                self.text_part,
                TextPart("━" * (seconds * fps - i), self.type_.color),
                TextPart("━" * i, Color.BG8),
            )

        yield EMPTY_TEXT

    @property
    def animation(self) -> TextAnimation:
        return TextAnimation(frames=self.animation_frames, fps=self.type_.animation_fps)


@frozen
class Keybind:
    """A single keybind."""

    key: str | tuple[str, ...]
    """Triggering key, or combination of keys."""

    display_key: str
    """Key that will be visible to the user, if the `key` is not user-friendly."""

    tooltip: str | None
    """Optional tooltip to show to the user."""

    action: Callable[[KeyPressEvent], None | Awaitable[None]] = field(eq=False)
    """Async action to call for this kebind."""

    is_hidden: bool = field(default=False)
    """If `True`, the keybind will not be visible to the user."""

    condition: Callable[[], bool] = field(default=lambda: True, eq=False)
    """Callable that returns whether the keybind should be active."""

    pt_filter: Filter = field(default=PtCondition(~buffer_has_focus), eq=False)
    """`prompt_toolkit` Filter to use."""


def remove_gameroom(
    gameroom_id: str | None, gamerooms: tuple[Gameroom, ...] | None
) -> tuple[Gameroom, ...]:
    """Remove a gameroom with the given id from the list of gamerooms.

    Does nothing if the gameroom is not present in the gamerooms list.

    Args:
        gameroom_id (str | None): The id of the gameroom to remove.
        gamerooms (tuple[Gameroom, ...] | None): The list of gamerooms
            to remove the gameroom from.

    Returns:
        A copy of the list without the removed gameroom.
    """
    _gamerooms: list[Gameroom] = list(gamerooms) if gamerooms else []
    if gameroom_id and (
        gameroom := first(
            (gameroom for gameroom in _gamerooms if gameroom.id == gameroom_id), None
        )
    ):
        _gamerooms.remove(gameroom)
    return tuple(_gamerooms)


class _TileNode(NamedTuple):
    id: int
    order: int


def sorted_tileset(tileset: list[int]) -> list[int]:
    deck_size = 52
    jokers = {104, 105}
    return [
        node.id
        for node in sorted(
            [
                _TileNode(id=tile, order=tile)
                if (tile < deck_size or tile in jokers)
                else _TileNode(id=tile, order=tile - deck_size)
                for tile in tileset
            ],
            key=lambda node: node.order,
        )
    ]
