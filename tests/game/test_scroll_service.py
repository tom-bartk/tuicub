from collections.abc import Callable
from unittest.mock import Mock

import pytest

from src.tuicub.game.models import ScrollDirection, Tile, Tileset
from src.tuicub.game.services.scroll_service import ScrollService, take_closest
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def tile() -> Callable[[int], Tile]:
    def factory(tile_id: int) -> Tile:
        return Tile.from_id(id=tile_id)

    return factory


@pytest.fixture()
def tileset() -> Callable[[[int, ...]], Tileset]:  # : valid-type
    def factory(*tile_ids: int) -> Tileset:
        return Tileset.from_tile_ids(tiles=list(tile_ids))

    return factory


@pytest.fixture()
def board(tileset) -> tuple[tuple[Tileset, ...], ...]:
    return (
        (tileset(1, 2, 3, 4, 5), tileset(6, 7, 8), tileset(9, 10, 11, 12)),
        (
            tileset(13, 14),
            tileset(15, 16, 17),
        ),
        (tileset(18, 19), tileset(20, 21, 22), tileset(23, 24, 25, 26)),
    )


@pytest.fixture()
def rack(tileset) -> Tileset:
    return tileset(27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37)


@pytest.fixture()
def virtual_tileset(tileset) -> Tileset:
    return tileset(27, 28, 29)


@pytest.fixture()
def highlighted_tile(tile) -> Callable[[int], GameScreenState]:
    def factory(tile_id: int) -> GameScreenState:
        return GameScreenState(highlighted_tile=tile(tile_id))

    return factory


@pytest.fixture()
def highlighted_tileset(tileset) -> Callable[[int], GameScreenState]:
    def factory(*tile_ids: int) -> GameScreenState:
        return GameScreenState(highlighted_tileset=tileset(*tile_ids))

    return factory


@pytest.fixture()
def sut(board, cache, screen_size_service, virtual_tileset, rack) -> ScrollService:
    screen_size_service.width = Mock(return_value=80)
    cache.get = Mock(return_value=None)
    sut = ScrollService(cache=cache, screen_size_service=screen_size_service)
    sut.update_scroll_maps(board=board, virtual_tileset=virtual_tileset, rack=rack)
    return sut


class TestScrollTiles:
    def test_when_no_highlighted_tile__returns_none(self, sut) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.DOWN, state=GameScreenState(highlighted_tile=None)
        )
        expected = None

        assert result == expected

    def test_when_down__from_left_edge__lower_row_less_tilesets__returns_left_edge(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.DOWN, state=highlighted_tile(1)
        )
        expected = tile(13)

        assert result == expected

    def test_when_down__from_right_edge__lower_row_less_tiles__returns_right_edge(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.DOWN, state=highlighted_tile(12)
        )
        expected = tile(17)

        assert result == expected

    def test_when_down__from_left_edge__lower_row_more_tiles__returns_tile_below(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.DOWN, state=highlighted_tile(13)
        )
        expected = tile(20)

        assert result == expected

    def test_when_down__from_right_edge__lower_row_more_tiles__returns_tile_below(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.DOWN, state=highlighted_tile(17)
        )
        expected = tile(24)

        assert result == expected

    def test_when_down__from_bottom_row__returns_tile_from_rack(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.DOWN, state=highlighted_tile(18)
        )
        expected = tile(27)

        assert result == expected

    def test_when_down__from_rack__returns_none(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.DOWN, state=highlighted_tile(28)
        )
        expected = None

        assert result == expected

    def test_when_up__from_left_edge__upper_row_less_tiles__returns_left_edge(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.UP, state=highlighted_tile(18)
        )
        expected = tile(13)

        assert result == expected

    def test_when_up__from_right_edge__upper_row_less_tiles__returns_right_edge(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.UP, state=highlighted_tile(26)
        )
        expected = tile(17)

        assert result == expected

    def test_when_up__from_left_edge__upper_row_more_tiles__returns_tile_above(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.UP, state=highlighted_tile(13)
        )
        expected = tile(5)

        assert result == expected

    def test_when_up__from_right_edge__upper_row_more_tiles__returns_tile_above(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.UP, state=highlighted_tile(17)
        )
        expected = tile(8)

        assert result == expected

    def test_when_up__from_top_row__returns_none(self, sut, highlighted_tile) -> None:
        result = sut.scroll_tiles(direction=ScrollDirection.UP, state=highlighted_tile(1))
        expected = None

        assert result == expected

    def test_when_up__from_rack__returns_tile_from_bottom_row(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.UP, state=highlighted_tile(27)
        )
        expected = tile(18)

        assert result == expected

    def test_when_left__from_right_edge__returns_tile_to_left(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.LEFT, state=highlighted_tile(12)
        )
        expected = tile(11)

        assert result == expected

    def test_when_left__from_left_edge__returns_none(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.LEFT, state=highlighted_tile(1)
        )
        expected = None

        assert result == expected

    def test_when_right__from_right_edge__returns_none(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.RIGHT, state=highlighted_tile(12)
        )
        expected = None

        assert result == expected

    def test_when_right__from_left_edge__returns_tile_to_right(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.RIGHT, state=highlighted_tile(1)
        )
        expected = tile(2)

        assert result == expected

    def test_when_tile_not_mapped__returns_none(
        self, sut, tile, highlighted_tile
    ) -> None:
        result = sut.scroll_tiles(
            direction=ScrollDirection.RIGHT, state=highlighted_tile(105)
        )
        expected = None

        assert result == expected


class TestScrollTilesets:
    def test_when_no_highlighted_tileset__returns_none(self, sut) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.DOWN,
            state=GameScreenState(highlighted_tileset=None),
        )
        expected = None

        assert result == expected

    def test_when_down__from_left_edge__lower_row_less_tilesets__returns_left_edge(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.DOWN, state=highlighted_tileset(1, 2, 3, 4, 5)
        )
        expected = tileset(13, 14)

        assert result == expected

    def test_when_down__from_right_edge__lower_row_less_tilesets__returns_right_edge(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.DOWN, state=highlighted_tileset(9, 10, 11, 12)
        )
        expected = tileset(15, 16, 17)

        assert result == expected

    def test_when_down__from_left_edge__lower_row_more_tilesets__returns_tileset_below(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.DOWN, state=highlighted_tileset(13, 14)
        )
        expected = tileset(20, 21, 22)

        assert result == expected

    def test_when_down__from_right_edge__lower_row_more_tilesets__returns_tileset_below(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.DOWN, state=highlighted_tileset(15, 16, 17)
        )
        expected = tileset(23, 24, 25, 26)

        assert result == expected

    def test_when_down__from_bottom_row__returns_virtual_tileset(
        self, sut, tileset, highlighted_tileset, virtual_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.DOWN, state=highlighted_tileset(18, 19)
        )
        expected = virtual_tileset

        assert result == expected

    def test_when_down__from_virtual_tileset__returns_none(
        self, sut, tileset, highlighted_tileset, virtual_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.DOWN,
            state=GameScreenState(
                virtual_tileset=virtual_tileset, highlighted_tileset=virtual_tileset
            ),
        )
        expected = None

        assert result == expected

    def test_when_up__from_left_edge__upper_row_less_tilesets__returns_left_edge(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.UP, state=highlighted_tileset(18, 19)
        )
        expected = tileset(13, 14)

        assert result == expected

    def test_when_up__from_right_edge__upper_row_less_tilesets__returns_right_edge(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.UP, state=highlighted_tileset(23, 24, 25, 26)
        )
        expected = tileset(15, 16, 17)

        assert result == expected

    def test_when_up__from_left_edge__upper_row_more_tilesets__returns_tileset_above(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.UP, state=highlighted_tileset(13, 14)
        )
        expected = tileset(1, 2, 3, 4, 5)

        assert result == expected

    def test_when_up__from_right_edge__upper_row_more_tilesets__returns_tileset_above(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.UP, state=highlighted_tileset(15, 16, 17)
        )
        expected = tileset(6, 7, 8)

        assert result == expected

    def test_when_up__from_top_row__returns_none(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.UP, state=highlighted_tileset(1, 2, 3, 4, 5)
        )
        expected = None

        assert result == expected

    def test_when_left__from_right_edge__returns_tileset_to_left(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.LEFT, state=highlighted_tileset(9, 10, 11, 12)
        )
        expected = tileset(6, 7, 8)

        assert result == expected

    def test_when_left__from_left_edge__returns_none(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.LEFT, state=highlighted_tileset(1, 2, 3, 4, 5)
        )
        expected = None

        assert result == expected

    def test_when_right__from_right_edge__returns_none(
        self, sut, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.RIGHT, state=highlighted_tileset(9, 10, 11, 12)
        )
        expected = None

        assert result == expected

    def test_when_right__from_left_edge__returns_tileset_to_right(
        self, sut, tileset, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.RIGHT, state=highlighted_tileset(1, 2, 3, 4, 5)
        )
        expected = tileset(6, 7, 8)

        assert result == expected

    def test_when_tileset_not_mapped__returns_none(
        self, sut, highlighted_tileset
    ) -> None:
        result = sut.scroll_tilesets(
            direction=ScrollDirection.RIGHT, state=highlighted_tileset(103, 104, 105)
        )
        expected = None

        assert result == expected


class TestUpdateScrollMaps:
    def test_when_maps_cached__does_not_cache_new_maps(
        self, sut, board, cache, screen_size_service, virtual_tileset, rack
    ) -> None:
        screen_size_service.width = Mock(return_value=80)
        cache.reset_mock()
        cache.get = Mock(return_value=(Mock(), Mock()))

        sut.update_scroll_maps(board=board, virtual_tileset=virtual_tileset, rack=rack)

        cache.set.assert_not_called()


class TestTakeClosest:
    def test_when_entries_empty__returns_none(self) -> None:
        expected = None

        result = take_closest(entries=[], value=Mock())

        assert result == expected
