import binpacking  # type: ignore[import]

from ...common.cache import Cache
from ...common.services.screen_size_service import ScreenSizeService
from ..models import Tileset


class BoardService:
    """A service for creating game boards.

    aa
    """

    __slots__ = ("_cache", "_screen_size_service")

    def __init__(self, cache: Cache, screen_size_service: ScreenSizeService):
        """Initialize new service.

        Args:
            cache (Cache): The cache for game boards.
            screen_size_service (ScreenSizeService): The screen size service.
        """
        self._cache: Cache = cache
        self._screen_size_service: ScreenSizeService = screen_size_service

    def create_rows(self, board: frozenset[Tileset]) -> tuple[tuple[Tileset, ...], ...]:
        """Create rows from the board.

        Returns a sequence of rows, which themselves are sequences of tilesets.
        Rows are calculated using a bin packing algorithm to minimize the number of rows
        needed to fit all tilesets on the screen.

        Results are cached based on a hash of the board and the screen width.

        Args:
            board (frozenset[Tileset]): The board to create rows for.

        Returns:
            The rows of tilesets created from the board.
        """
        width = self._screen_size_service.width()
        if cached := self._cache.get(hash((board, width)), default=None):
            return cached
        else:
            rows = tuple(
                tuple(bin.keys())
                for bin in binpacking.to_constant_volume(
                    {tileset: tileset.width() for tileset in board}, width
                )
            )
            self._cache.set(hash((board, width)), rows)

            return rows
