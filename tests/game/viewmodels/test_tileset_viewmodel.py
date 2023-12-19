import pytest

from src.tuicub.game.consts import TILE_WIDTH
from src.tuicub.game.viewmodels.tile import TileViewModel
from src.tuicub.game.viewmodels.tileset import TILESET_SPACING, TilesetViewModel


@pytest.fixture()
def sut(tile) -> TilesetViewModel:
    return TilesetViewModel(
        tiles=(
            TileViewModel(
                tile=tile(1), is_selected=False, is_highlighted=False, is_new=False
            ),
            TileViewModel(
                tile=tile(2), is_selected=False, is_highlighted=False, is_new=False
            ),
            TileViewModel(
                tile=tile(3), is_selected=False, is_highlighted=False, is_new=False
            ),
        ),
        is_highlighted=False,
    )


class TestWidth:
    def test_returns_tile_width_times_tiles_count_plus_double_spacing(self, sut) -> None:
        expected = 3 * TILE_WIDTH + TILESET_SPACING * 2

        result = sut.width()

        assert result == expected
