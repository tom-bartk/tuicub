from __future__ import annotations

from bisect import bisect_left
from collections.abc import Callable, Hashable, Iterable, MutableSequence, Sequence
from typing import Generic, TypeVar

from attrs import field, frozen

from ...common.cache import Cache
from ...common.services.screen_size_service import ScreenSizeService
from ..consts import TILE_WIDTH
from ..models import ScrollDirection, Tile, Tileset
from ..state import GameScreenState

T = TypeVar("T", covariant=True)
THashable = TypeVar("THashable", bound=Hashable)


class ScrollService:
    """A service for scrolling tiles and tilesets on the game board."""

    __slot__ = (
        "_cache",
        "_tiles_scroll_map",
        "_tilesets_scroll_map",
        "_screen_size_service",
    )

    def __init__(self, cache: Cache, screen_size_service: ScreenSizeService):
        """Initialize new service.

        Args:
            cache (Cache): The cache for scroll maps.
            screen_size_service (ScreenSizeService): The screen size service.
        """
        self._tiles_scroll_map: dict[Tile, ScrollNode[Tile]] = {}
        self._tilesets_scroll_map: dict[Tileset, ScrollNode[Tileset]] = {}
        self._screen_size_service: ScreenSizeService = screen_size_service
        self._cache: Cache = cache

    def update_scroll_maps(
        self,
        board: tuple[tuple[Tileset, ...], ...],
        virtual_tileset: Tileset,
        rack: Tileset,
    ) -> None:
        """Update scroll maps for new board and rack.

        Every tile on the board and rack, and every played tileset has a corresponding
        scroll node, which holds neighbouring tiles/tilesets for up, down, left and right
        scrolling directions.

        Args:
            board (tuple[tuple[Tileset, ...], ...]): The new board.
            virtual_tileset (Tileset): The current virtual tileset.
            rack (Tileset): The new rack.
        """
        width = self._screen_size_service.width()
        key = hash((board, virtual_tileset, rack, width))
        if maps := self._cache.get(key, None):
            self._tiles_scroll_map, self._tilesets_scroll_map = maps
        else:
            self._tiles_scroll_map = create_tiles_scroll_map(
                board=board, rack=rack, screen_width=width
            )
            self._tilesets_scroll_map = create_tilesets_scroll_map(
                board=board, virtual_tileset=virtual_tileset, screen_width=width
            )
            self._cache.set(key, (self._tiles_scroll_map, self._tilesets_scroll_map))

    def scroll_tiles(
        self, direction: ScrollDirection, state: GameScreenState
    ) -> Tile | None:
        """Scroll tiles in the given direction.

        Returns a tile that should be highlighted after performing the scroll
        in the given direction, or None if there is no possible tile to scroll to.
        The next tile is chosen based on the current scroll map and the direction.

        Args:
            direction (ScrollDirection): The direction of the scroll.
            state (GameScreenState): The current state of the game screen.

        Returns:
            The next tile to higlight, or None if scrolling is not possible.
        """
        return self._scroll(
            current=state.highlighted_tile,
            direction=direction,
            scroll_map=self._tiles_scroll_map,
        )

    def scroll_tilesets(
        self, direction: ScrollDirection, state: GameScreenState
    ) -> Tileset | None:
        """Scroll tilesets in the given direction.

        Returns a tileset that should be highlighted after performing the scroll
        in the given direction, or None if there is no possible tileset to scroll to.
        The next tileset is chosen based on the current scroll map and the direction.

        Args:
            direction (ScrollDirection): The direction of the scroll.
            state (GameScreenState): The current state of the game screen.

        Returns:
            The next tileset to higlight, or None if scrolling is not possible.
        """
        return self._scroll(
            current=state.highlighted_tileset,
            direction=direction,
            scroll_map=self._tilesets_scroll_map,
        )

    def _scroll(
        self,
        current: THashable | None,
        direction: ScrollDirection,
        scroll_map: dict[THashable, ScrollNode[THashable]],
    ) -> THashable | None:
        if not current:
            return None

        node: ScrollNode[THashable] | None = scroll_map.get(current, None)
        if not node:
            return None

        _next: THashable | None = None
        if direction == ScrollDirection.LEFT:
            _next = node.left
        elif direction == ScrollDirection.RIGHT:
            _next = node.right
        elif direction == ScrollDirection.UP:
            _next = node.top
        elif direction == ScrollDirection.DOWN:
            _next = node.bottom
        if not _next:
            return None

        return _next


@frozen
class ScrollNode(Generic[THashable]):
    """A scroll map node holding neighbouring elements."""

    value: THashable
    top: THashable | None = field(default=None)
    right: THashable | None = field(default=None)
    bottom: THashable | None = field(default=None)
    left: THashable | None = field(default=None)


TKey = TypeVar("TKey", bound=Hashable)
TVal = TypeVar("TVal")


class EdgeDistance(Generic[T]):
    """A distance of a tile/tileset from the left edge of the screen."""

    __slots__ = ("_distance", "_value")

    @property
    def distance(self) -> int:
        """The distance from the left edge of the screen in characters."""
        return self._distance

    @property
    def value(self) -> T:
        """The tile or tileset."""
        return self._value

    def __init__(self, distance: int, value: T):
        self._distance: int = distance
        self._value: T = value

    def __eq__(self, other: object) -> bool:  # pragma: no cover
        if not isinstance(other, EdgeDistance):
            return NotImplemented

        return self.distance == other.distance and self.value == other.value

    def __hash__(self) -> int:  # pragma: no cover
        return hash((self.value, self.distance))


@frozen
class AdjacentEdges(Generic[T]):
    """A container for adjacent edge distances of a tile or tileset."""

    bottom: EdgeDistance[T] | None
    left: EdgeDistance[T] | None
    right: EdgeDistance[T] | None
    top: EdgeDistance[T] | None


def create_tiles_scroll_map(
    board: tuple[tuple[Tileset, ...], ...],
    rack: Tileset,
    screen_width: int,
) -> dict[Tile, ScrollNode[Tile]]:
    return dict(
        nodes_matrix(
            distances_matrix=distances_matrix(
                board_rows=board,
                bottom_row=rack,
                screen_width=screen_width,
                tileset_to_distances=tiles_tileset_to_distances,
            ),
            node_factory=tile_node,
        )
    )


def create_tilesets_scroll_map(
    board: tuple[tuple[Tileset, ...], ...], virtual_tileset: Tileset, screen_width: int
) -> dict[Tileset, ScrollNode[Tileset]]:
    return dict(
        nodes_matrix(
            distances_matrix=distances_matrix(
                board_rows=board,
                bottom_row=virtual_tileset,
                screen_width=screen_width,
                tileset_to_distances=tilesets_tileset_to_distances,
            ),
            node_factory=tileset_node,
        )
    )


def tiles_tileset_to_distances(
    tileset: Tileset, current_distance: int
) -> Sequence[EdgeDistance[Tile]]:
    return tuple(
        EdgeDistance(distance=current_distance + (index * TILE_WIDTH), value=tile)
        for index, tile in enumerate(tileset.tiles)
    )


def tilesets_tileset_to_distances(
    tileset: Tileset, current_distance: int
) -> Sequence[EdgeDistance[Tileset]]:
    return (
        EdgeDistance(distance=current_distance + (tileset.width() // 2), value=tileset),
    )


def distances_matrix(
    board_rows: tuple[tuple[Tileset, ...], ...],
    bottom_row: Tileset,
    screen_width: int,
    tileset_to_distances: Callable[[Tileset, int], Sequence[EdgeDistance[T]]],
) -> Sequence[Sequence[EdgeDistance[T]]]:
    _distances_matrix: MutableSequence[Sequence[EdgeDistance[T]]] = []
    for row in combine_rows(board_rows, bottom_row):
        current_distance = leftmost_distance(row, screen_width)
        distances: list[EdgeDistance[T]] = []
        for tileset in row:
            distances.extend(tileset_to_distances(tileset, current_distance))
            current_distance += tileset.width()

        _distances_matrix.append(distances)
    return _distances_matrix


def combine_rows(
    board_rows: tuple[tuple[Tileset, ...], ...], bottom_row: Tileset
) -> tuple[tuple[Tileset, ...], ...]:
    return ((bottom_row,), *tuple(reversed(board_rows)))


def leftmost_distance(row: tuple[Tileset, ...], screen_width: int) -> int:
    return (screen_width - row_width(row)) // 2


def row_width(row: tuple[Tileset, ...]) -> int:
    return sum(tileset.width() for tileset in row)


def nodes_matrix(
    distances_matrix: Sequence[Sequence[EdgeDistance[T]]],
    node_factory: Callable[
        [EdgeDistance[T], AdjacentEdges[T]],
        tuple[TKey, ScrollNode[TVal]],
    ],
) -> Iterable[tuple[TKey, ScrollNode[TVal]]]:
    _nodes_matrix: list[tuple[TKey, ScrollNode[TVal]]] = []
    for row_index, row in enumerate(distances_matrix):
        for entry_index, entry in enumerate(row):
            _nodes_matrix.append(
                node_factory(
                    entry,
                    adjacent_edges(distances_matrix, row, row_index, entry, entry_index),
                )
            )
    return _nodes_matrix


def adjacent_edges(
    distances_matrix: Sequence[Sequence[EdgeDistance[T]]],
    row: Sequence[EdgeDistance[T]],
    row_index: int,
    entry: EdgeDistance[T],
    entry_index: int,
) -> AdjacentEdges[T]:
    top: EdgeDistance[T] | None = None
    right: EdgeDistance[T] | None = None
    bottom: EdgeDistance[T] | None = None
    left: EdgeDistance[T] | None = None

    if entry_index > 0:
        left = row[entry_index - 1]
    if entry_index < len(row) - 1:
        right = row[entry_index + 1]
    if row_index > 0 and distances_matrix[row_index - 1]:
        bottom = take_closest(distances_matrix[row_index - 1], entry)
    if row_index < len(distances_matrix) - 1:
        top = take_closest(distances_matrix[row_index + 1], entry)
    return AdjacentEdges(bottom, left, right, top)


def take_closest(
    entries: Sequence[EdgeDistance], value: EdgeDistance
) -> EdgeDistance | None:
    if not entries:
        return None
    distances: list[int] = [entry.distance for entry in entries]
    pos = bisect_left(distances, value.distance)
    if pos == 0:
        return entries[0]
    if pos == len(distances):
        return entries[-1]
    before = distances[pos - 1]
    after = distances[pos]
    if after - value.distance < value.distance - before:
        return entries[pos]
    else:
        return entries[pos - 1]


def tile_node(
    edge: EdgeDistance[Tile],
    adjacent_edges: AdjacentEdges[Tile],
) -> tuple[Tile, ScrollNode[Tile]]:
    return edge.value, ScrollNode(
        edge.value,
        top=None if not adjacent_edges.top else adjacent_edges.top.value,
        right=None if not adjacent_edges.right else adjacent_edges.right.value,
        bottom=None if not adjacent_edges.bottom else adjacent_edges.bottom.value,
        left=None if not adjacent_edges.left else adjacent_edges.left.value,
    )


def tileset_node(
    edge: EdgeDistance[Tileset],
    adjacent_edges: AdjacentEdges[Tileset],
) -> tuple[Tileset, ScrollNode[Tileset]]:
    return edge.value, ScrollNode(
        edge.value,
        top=None if not adjacent_edges.top else adjacent_edges.top.value,
        right=None if not adjacent_edges.right else adjacent_edges.right.value,
        bottom=None if not adjacent_edges.bottom else adjacent_edges.bottom.value,
        left=None if not adjacent_edges.left else adjacent_edges.left.value,
    )
