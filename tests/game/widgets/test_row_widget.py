from src.tuicub.common.views import Color
from src.tuicub.game.consts import TILESET_HEIGHT
from src.tuicub.game.widgets.renderer import HorizontalPosition
from src.tuicub.game.widgets.row import RowWidget
from src.tuicub.game.widgets.tileset import TilesetWidget


class TestRender:
    def test_renders_tileset_centrally(
        self, theme, screen, frame, renderer, tileset_vm, tile_vm
    ) -> None:
        tileset_1 = tileset_vm(tile_vm(1), tile_vm(2), tile_vm(3))
        tileset_2 = tileset_vm(tile_vm(3), tile_vm(4), tile_vm(5))
        tileset_3 = tileset_vm(tile_vm(6), tile_vm(7), tile_vm(8))
        tilesets = (
            TilesetWidget(viewmodel=tileset_1, parent_background=Color.BG2, theme=theme),
            TilesetWidget(viewmodel=tileset_2, parent_background=Color.BG2, theme=theme),
            TilesetWidget(viewmodel=tileset_3, parent_background=Color.BG2, theme=theme),
        )
        sut = RowWidget(tilesets=(tileset_1, tileset_2, tileset_3), theme=theme)

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_horizontally.assert_called_once_with(
            tilesets, HorizontalPosition.CENTER, frame, screen
        )


class TestHeight:
    def test_returns_correct_height(self, theme) -> None:
        expected = TILESET_HEIGHT
        sut = RowWidget(tilesets=(), theme=theme)

        result = sut.height

        assert result == expected
