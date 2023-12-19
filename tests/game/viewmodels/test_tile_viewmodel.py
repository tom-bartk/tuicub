from collections.abc import Callable
from unittest.mock import create_autospec

import pytest

from src.tuicub.common.views import Color, Theme
from src.tuicub.game.models import Tile
from src.tuicub.game.viewmodels.tile import TileViewModel, VirtualTileViewModel


@pytest.fixture()
def theme() -> Theme:
    return create_autospec(Theme)


@pytest.fixture()
def make_sut() -> Callable[[Tile, bool, bool, bool], TileViewModel]:
    def factory(
        tile: Tile,
        is_selected: bool = False,
        is_highlighted: bool = False,
        is_new: bool = False,
    ) -> TileViewModel:
        return TileViewModel(
            tile=tile,
            is_selected=is_selected,
            is_highlighted=is_highlighted,
            is_new=is_new,
        )

    return factory


class TestTileViewModel:
    @pytest.fixture()
    def make_sut(self) -> Callable[[Tile, bool, bool, bool], TileViewModel]:
        def factory(
            tile: Tile,
            is_selected: bool = False,
            is_highlighted: bool = False,
            is_new: bool = False,
        ) -> TileViewModel:
            return TileViewModel(
                tile=tile,
                is_selected=is_selected,
                is_highlighted=is_highlighted,
                is_new=is_new,
            )

        return factory

    def test_content__returns_correct_content(self, make_sut, tile, theme) -> None:
        expected = [
            ("style", "▗▄▄▖\n"),
            ("style", "▌"),
            ("style", "1 "),
            ("style", "▌\n"),
            ("style", "▝▀▀▘"),
        ]
        theme.style.return_value = "style"
        sut = make_sut(tile(0))

        result = sut.content(parent_background=Color.BG3, theme=theme)

        assert result == expected


class TestVirtualTileViewModel:
    @pytest.fixture()
    def make_sut(self) -> Callable[[Tile, bool, bool, bool], VirtualTileViewModel]:
        def factory(
            tile: Tile,
            is_selected: bool = False,
            is_highlighted: bool = False,
            is_new: bool = False,
        ) -> VirtualTileViewModel:
            return VirtualTileViewModel(
                tile=tile,
                is_selected=is_selected,
                is_highlighted=is_highlighted,
                is_new=is_new,
            )

        return factory

    def test_content__returns_correct_content(self, make_sut, tile, theme) -> None:
        expected = [
            ("style", "▗▄▄▖\n"),
            ("style", "▌"),
            ("style", "  "),
            ("style", "▌\n"),
            ("style", "▝▀▀▘"),
        ]
        theme.style.return_value = "style"
        sut = make_sut(tile(0))

        result = sut.content(parent_background=Color.BG3, theme=theme)

        assert result == expected
