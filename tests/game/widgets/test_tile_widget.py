from unittest.mock import Mock, create_autospec

import pytest

from src.tuicub.common.views import Color
from src.tuicub.game.consts import TILE_HEIGHT, TILE_WIDTH
from src.tuicub.game.viewmodels.tile import TileViewModel
from src.tuicub.game.widgets.tile import TileWidget


@pytest.fixture()
def parent_background(tile_vm) -> Color:
    return Color.BG2


@pytest.fixture()
def viewmodel() -> TileViewModel:
    return create_autospec(TileViewModel)


@pytest.fixture()
def sut(viewmodel, theme, parent_background) -> TileWidget:
    return TileWidget(
        viewmodel=viewmodel, parent_background=parent_background, theme=theme
    )


class TestRender:
    def test_writes_viewmodel_content(
        self, sut, theme, renderer, screen, viewmodel, frame, parent_background
    ) -> None:
        content = Mock()
        viewmodel.content.return_value = content

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.write_content.assert_called_once_with(content, frame, screen)
        viewmodel.content.assert_called_once_with(
            parent_background=parent_background, theme=theme
        )


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = TILE_HEIGHT

        result = sut.height

        assert result == expected


class TestWidth:
    def test_returns_correct_width(self, sut) -> None:
        expected = TILE_WIDTH

        result = sut.width

        assert result == expected
