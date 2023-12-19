from attrs import frozen

from ..consts import TILE_WIDTH
from .tile import TileViewModel

TILESET_SPACING = 1


@frozen
class TilesetViewModel:
    """A viewmodel for a tileset widget.

    Attributes:
        tiles (tuple[TilesetViewModel, ...]): Tiles making this tileset.
        is_highlighted (bool): Whether the tileset is currently highlighted.
    """

    tiles: tuple[TileViewModel, ...]
    is_highlighted: bool

    def width(self) -> int:
        """Returns the current width in characters of the tileset."""
        return len(self.tiles) * TILE_WIDTH + TILESET_SPACING * 2
