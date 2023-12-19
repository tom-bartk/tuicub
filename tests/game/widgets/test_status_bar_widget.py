from unittest.mock import Mock, create_autospec

import pytest

from src.tuicub.common.views import Color
from src.tuicub.game.viewmodels.status_bar import StatusBarViewModel
from src.tuicub.game.widgets.status_bar import HEIGHT, StatusBarWidget


@pytest.fixture()
def viewmodel() -> StatusBarViewModel:
    return create_autospec(StatusBarViewModel)


@pytest.fixture()
def sut(viewmodel, theme) -> StatusBarWidget:
    return StatusBarWidget(viewmodel=viewmodel, theme=theme)


class TestRender:
    def test_writes_viewmodel_content(
        self, sut, theme, viewmodel, screen, frame, renderer
    ) -> None:
        content = Mock()
        viewmodel.content.return_value = content

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.write_content.assert_called_once_with(content, frame, screen)

    def test_sets_background_color_to_viewmodel_bar_bg_color(
        self, sut, viewmodel, screen, frame, renderer
    ) -> None:
        bar_bg_color = Color.YELLOW
        viewmodel.bar_bg_color.return_value = bar_bg_color

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.set_background_color.assert_called_once_with(Color.YELLOW, screen, frame)


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = HEIGHT

        result = sut.height

        assert result == expected
