import pytest

from src.tuicub.common.views import Color
from src.tuicub.game.consts import TILESET_HEIGHT
from src.tuicub.game.viewmodels.tileset import TilesetViewModel
from src.tuicub.game.widgets.rack import RackWidget
from src.tuicub.game.widgets.renderer import Position, SeparatorSide, Side
from src.tuicub.game.widgets.tileset import TilesetWidget


@pytest.fixture()
def viewmodel(tileset_vm, tile_vm) -> TilesetViewModel:
    return tileset_vm(tile_vm(1), tile_vm(2), tile_vm(3))


@pytest.fixture()
def sut(viewmodel, theme) -> RackWidget:
    return RackWidget(viewmodel=viewmodel, theme=theme)


class TestRender:
    def test_renders_tileset_centrally(
        self, sut, theme, viewmodel, screen, frame, renderer
    ) -> None:
        tileset = TilesetWidget(
            viewmodel=viewmodel, parent_background=Color.BG3, theme=theme
        )

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_widget.assert_called_once_with(
            tileset,
            position=Position.CENTER,
            side=Side.CENTER,
            screen=screen,
            frame=frame,
        )

    def test_draws_top_separator(self, sut, screen, frame, renderer) -> None:
        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.draw_separator.assert_called_once_with(SeparatorSide.TOP, frame, screen)

    def test_sets_background_color_to_bg3(self, sut, screen, frame, renderer) -> None:
        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.set_background_color.assert_called_once_with(Color.BG3, screen, frame)


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = TILESET_HEIGHT

        result = sut.height

        assert result == expected
