from __future__ import annotations

from enum import IntEnum, StrEnum

from attrs import field, frozen

from ..common.views import Color as UIColor
from .consts import TILE_WIDTH


class ScrollDirection(IntEnum):
    """The scrolling direction of the game board."""

    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Color(IntEnum):
    """The color of the tile."""

    RED = 1
    YELLOW = 2
    BLUE = 3
    BLACK = 4

    @property
    def ui_color(self) -> UIColor:
        """Returns the UI tile color."""
        match self:
            case Color.RED:
                return UIColor.TILE_RED
            case Color.YELLOW:
                return UIColor.TILE_YELLOW
            case Color.BLUE:
                return UIColor.TILE_BLUE
            case Color.BLACK:
                return UIColor.TILE_BLACK

    @property
    def ui_selected_color(self) -> UIColor:
        """Returns the UI tile color for the selected state."""
        match self:
            case Color.RED | Color.YELLOW | Color.BLUE:
                return self.ui_color
            case Color.BLACK:
                return UIColor.TILE_BLACK_SELECTED


class SelectionMode(StrEnum):
    """The selection mode."""

    TILES = "TILES"
    TILESETS = "TILESETS"


@frozen
class Tile:
    """Represent a single game tile.

    Attributes:
        id (int): The id of the tile.
        numer (int): The numerical value of the tile.
        color (int): The color of the tile.
        figure (int): The figure of the tile. Either 1 or 2.
    """

    id: int
    number: int
    color: Color
    figure: int

    @classmethod
    def from_id(cls, id: int) -> Tile:
        """Returns a tile for the given id."""
        return TILES[id]

    def is_joker(self) -> bool:
        """Returns true if the tile is a joker."""
        joker_ids = {104, 105}
        return self.id in joker_ids

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tile):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return f"[{self.id}] {self.number} {self.color.name}({self.figure})"


@frozen
class Tileset:
    """A set of played game tiles.

    Attributes:
        tiles (tuple[Tile, ...]): The tiles making this set.
    """

    tiles: tuple[Tile, ...] = field(default=())

    def width(self) -> int:
        """Returns the width (number of terminal characters) of the set."""
        padding = 1
        return len(self.tiles) * TILE_WIDTH + (padding * 2)

    @classmethod
    def from_tile_ids(cls, tiles: list[int]) -> Tileset:
        """Returns a tileset for the given list of tiles ids."""
        return Tileset(tiles=tuple(Tile.from_id(tile) for tile in tiles))

    def __str__(self) -> str:
        return str([str(tile) for tile in self.tiles])


@frozen(repr=False)
class VirtualTileset(Tileset):
    """Represents a tileset that will be created by moving selected tiles."""


@frozen
class Board:
    """A game board containing all played tilesets.

    Attributes:
        tilesets (frozenset[Tileset]): All played sets of tiles.
    """

    tilesets: frozenset[Tileset] = field(default=frozenset())


@frozen
class Player:
    """The representation of a user in a game.

    Attributes:
        name (str): The name of the player.
        user_id (str): The id of the user this player represents.
        tiles_count (int): The current count of tiles in the player's rack.
        has_turn (bool): True if the player currently has turn, false otherwise.
    """

    name: str
    user_id: str
    tiles_count: int = field(default=0)
    has_turn: bool = field(default=False)


TILES = [
    Tile(0, 1, Color.RED, 1),
    Tile(1, 2, Color.RED, 1),
    Tile(2, 3, Color.RED, 1),
    Tile(3, 4, Color.RED, 1),
    Tile(4, 5, Color.RED, 1),
    Tile(5, 6, Color.RED, 1),
    Tile(6, 7, Color.RED, 1),
    Tile(7, 8, Color.RED, 1),
    Tile(8, 9, Color.RED, 1),
    Tile(9, 10, Color.RED, 1),
    Tile(10, 11, Color.RED, 1),
    Tile(11, 12, Color.RED, 1),
    Tile(12, 13, Color.RED, 1),
    Tile(13, 1, Color.BLUE, 1),
    Tile(14, 2, Color.BLUE, 1),
    Tile(15, 3, Color.BLUE, 1),
    Tile(16, 4, Color.BLUE, 1),
    Tile(17, 5, Color.BLUE, 1),
    Tile(18, 6, Color.BLUE, 1),
    Tile(19, 7, Color.BLUE, 1),
    Tile(20, 8, Color.BLUE, 1),
    Tile(21, 9, Color.BLUE, 1),
    Tile(22, 10, Color.BLUE, 1),
    Tile(23, 11, Color.BLUE, 1),
    Tile(24, 12, Color.BLUE, 1),
    Tile(25, 13, Color.BLUE, 1),
    Tile(26, 1, Color.YELLOW, 1),
    Tile(27, 2, Color.YELLOW, 1),
    Tile(28, 3, Color.YELLOW, 1),
    Tile(29, 4, Color.YELLOW, 1),
    Tile(30, 5, Color.YELLOW, 1),
    Tile(31, 6, Color.YELLOW, 1),
    Tile(32, 7, Color.YELLOW, 1),
    Tile(33, 8, Color.YELLOW, 1),
    Tile(34, 9, Color.YELLOW, 1),
    Tile(35, 10, Color.YELLOW, 1),
    Tile(36, 11, Color.YELLOW, 1),
    Tile(37, 12, Color.YELLOW, 1),
    Tile(38, 13, Color.YELLOW, 1),
    Tile(39, 1, Color.BLACK, 1),
    Tile(40, 2, Color.BLACK, 1),
    Tile(41, 3, Color.BLACK, 1),
    Tile(42, 4, Color.BLACK, 1),
    Tile(43, 5, Color.BLACK, 1),
    Tile(44, 6, Color.BLACK, 1),
    Tile(45, 7, Color.BLACK, 1),
    Tile(46, 8, Color.BLACK, 1),
    Tile(47, 9, Color.BLACK, 1),
    Tile(48, 10, Color.BLACK, 1),
    Tile(49, 11, Color.BLACK, 1),
    Tile(50, 12, Color.BLACK, 1),
    Tile(51, 13, Color.BLACK, 1),
    Tile(52, 1, Color.RED, 2),
    Tile(53, 2, Color.RED, 2),
    Tile(54, 3, Color.RED, 2),
    Tile(55, 4, Color.RED, 2),
    Tile(56, 5, Color.RED, 2),
    Tile(57, 6, Color.RED, 2),
    Tile(58, 7, Color.RED, 2),
    Tile(59, 8, Color.RED, 2),
    Tile(60, 9, Color.RED, 2),
    Tile(61, 10, Color.RED, 2),
    Tile(62, 11, Color.RED, 2),
    Tile(63, 12, Color.RED, 2),
    Tile(64, 13, Color.RED, 2),
    Tile(65, 1, Color.BLUE, 2),
    Tile(66, 2, Color.BLUE, 2),
    Tile(67, 3, Color.BLUE, 2),
    Tile(68, 4, Color.BLUE, 2),
    Tile(69, 5, Color.BLUE, 2),
    Tile(70, 6, Color.BLUE, 2),
    Tile(71, 7, Color.BLUE, 2),
    Tile(72, 8, Color.BLUE, 2),
    Tile(73, 9, Color.BLUE, 2),
    Tile(74, 10, Color.BLUE, 2),
    Tile(75, 11, Color.BLUE, 2),
    Tile(76, 12, Color.BLUE, 2),
    Tile(77, 13, Color.BLUE, 2),
    Tile(78, 1, Color.YELLOW, 2),
    Tile(79, 2, Color.YELLOW, 2),
    Tile(80, 3, Color.YELLOW, 2),
    Tile(81, 4, Color.YELLOW, 2),
    Tile(82, 5, Color.YELLOW, 2),
    Tile(83, 6, Color.YELLOW, 2),
    Tile(84, 7, Color.YELLOW, 2),
    Tile(85, 8, Color.YELLOW, 2),
    Tile(86, 9, Color.YELLOW, 2),
    Tile(87, 10, Color.YELLOW, 2),
    Tile(88, 11, Color.YELLOW, 2),
    Tile(89, 12, Color.YELLOW, 2),
    Tile(90, 13, Color.YELLOW, 2),
    Tile(91, 1, Color.BLACK, 2),
    Tile(92, 2, Color.BLACK, 2),
    Tile(93, 3, Color.BLACK, 2),
    Tile(94, 4, Color.BLACK, 2),
    Tile(95, 5, Color.BLACK, 2),
    Tile(96, 6, Color.BLACK, 2),
    Tile(97, 7, Color.BLACK, 2),
    Tile(98, 8, Color.BLACK, 2),
    Tile(99, 9, Color.BLACK, 2),
    Tile(100, 10, Color.BLACK, 2),
    Tile(101, 11, Color.BLACK, 2),
    Tile(102, 12, Color.BLACK, 2),
    Tile(103, 13, Color.BLACK, 2),
    Tile(104, 14, Color.RED, 1),
    Tile(105, 14, Color.BLACK, 1),
]
