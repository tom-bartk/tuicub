from unittest.mock import create_autospec

import pytest

from src.tuicub.common.views import Color
from src.tuicub.game.consts import TILESET_HEIGHT
from src.tuicub.game.viewmodels.tile import TileViewModel
from src.tuicub.game.viewmodels.tileset import TilesetViewModel
from src.tuicub.game.widgets.renderer import HorizontalPosition
from src.tuicub.game.widgets.tile import TileWidget
from src.tuicub.game.widgets.tileset import (
    HORIZONTAL_PADDING,
    VERTICAL_PADDING,
    TilesetWidget,
)


@pytest.fixture()
def parent_background(tile_vm) -> Color:
    return Color.BG2


@pytest.fixture()
def tile1(tile_vm) -> TileViewModel:
    return tile_vm(1)


@pytest.fixture()
def tile2(tile_vm) -> TileViewModel:
    return tile_vm(2)


@pytest.fixture()
def tile3(tile_vm) -> TileViewModel:
    return tile_vm(3)


@pytest.fixture()
def viewmodel(tile1, tile2, tile3) -> TileViewModel:
    vm = create_autospec(TilesetViewModel)
    vm.tiles = (tile1, tile2, tile3)
    return vm


@pytest.fixture()
def sut(viewmodel, theme, parent_background) -> TilesetWidget:
    return TilesetWidget(
        viewmodel=viewmodel, parent_background=parent_background, theme=theme
    )


class TestRender:
    def test_when_not_highlighted__does_not_draw_border(
        self, sut, theme, renderer, screen, viewmodel, frame
    ) -> None:
        viewmodel.is_highlighted = False

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.draw_border.assert_not_called()

    def test_when_highlighted__draws_border(
        self, sut, theme, renderer, screen, viewmodel, frame
    ) -> None:
        viewmodel.is_highlighted = True

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.draw_border.assert_called_once_with(frame, screen)

    def test_renders_tiles_horizontally_from_left_to_right(
        self, sut, theme, renderer, screen, frame, tile1, tile2, tile3, parent_background
    ) -> None:
        tiles = (
            TileWidget(viewmodel=tile1, parent_background=parent_background, theme=theme),
            TileWidget(viewmodel=tile2, parent_background=parent_background, theme=theme),
            TileWidget(viewmodel=tile3, parent_background=parent_background, theme=theme),
        )

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_horizontally.assert_called_once_with(
            widgets=tiles,
            position=HorizontalPosition.LEFT,
            frame=frame,
            screen=screen,
            x_offset=HORIZONTAL_PADDING,
            y_offset=VERTICAL_PADDING,
        )


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = TILESET_HEIGHT

        result = sut.height

        assert result == expected


class TestWidth:
    def test_returns_viewmodel_width(self, sut, viewmodel) -> None:
        viewmodel.width.return_value = 42
        expected = 42

        result = sut.width

        assert result == expected
