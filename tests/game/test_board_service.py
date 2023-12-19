from unittest.mock import Mock, patch

import pytest

from src.tuicub.game.services.board_service import BoardService


@pytest.fixture()
def sut(cache, screen_size_service) -> BoardService:
    return BoardService(cache=cache, screen_size_service=screen_size_service)


class TestCreateRows:
    def test_when_cached__returns_cached_value(
        self, sut, cache, screen_size_service, tileset
    ) -> None:
        screen_size_service.width.return_value = 42
        board = frozenset({tileset(1, 2, 3), tileset(4, 5, 6)})
        key = hash((board, 42))
        expected = Mock()
        cache.get = Mock(return_value=expected)

        result = sut.create_rows(board=board)

        assert result == expected
        cache.get.assert_called_once_with(key, default=None)

    def test_when_not_cached__returns_result_of_bin_packing(
        self, sut, cache, screen_size_service, tileset
    ) -> None:
        with patch(
            "binpacking.to_constant_volume",
            return_value=[{tileset(1, 2, 3): 42}, {tileset(4, 5, 6): 42}],
        ):
            screen_size_service.width.return_value = 42
            board = frozenset({tileset(1, 2, 3), tileset(4, 5, 6)})
            cache.get = Mock(return_value=None)
            expected = ((tileset(1, 2, 3),), (tileset(4, 5, 6),))

            result = sut.create_rows(board=board)

            assert result == expected

    def test_when_not_cached__caches_result(
        self, sut, cache, screen_size_service, tileset
    ) -> None:
        with patch(
            "binpacking.to_constant_volume",
            return_value=[{tileset(1, 2, 3): 42}, {tileset(4, 5, 6): 42}],
        ):
            screen_size_service.width.return_value = 42
            board = frozenset({tileset(1, 2, 3), tileset(4, 5, 6)})
            key = hash((board, 42))
            cache.get = Mock(return_value=None)
            expected = ((tileset(1, 2, 3),), (tileset(4, 5, 6),))

            sut.create_rows(board=board)

            cache.set.assert_called_once_with(key, expected)
