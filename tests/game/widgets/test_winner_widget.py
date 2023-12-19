from unittest.mock import Mock, create_autospec, patch

import pytest

from src.tuicub.common.views import Color
from src.tuicub.game.viewmodels.winner import WinnerViewModel
from src.tuicub.game.widgets.player import HEIGHT
from src.tuicub.game.widgets.winner import HORIZONTAL_PADDING, WinnerWidget


@pytest.fixture()
def viewmodel() -> WinnerViewModel:
    return create_autospec(WinnerViewModel)


@pytest.fixture()
def sut(viewmodel, theme) -> WinnerWidget:
    return WinnerWidget(viewmodel=viewmodel, theme=theme)


class TestRender:
    def test_writes_viewmodel_centered_content(
        self, sut, theme, renderer, screen, viewmodel, frame
    ) -> None:
        content = Mock()
        viewmodel.content.return_value = content

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.write_centered_content.assert_called_once_with(content, frame, screen)
        viewmodel.content.assert_called_once_with(theme=theme)

    def test_sets_background_color_to_bg3(self, sut, screen, frame, renderer) -> None:
        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.set_background_color.assert_called_once_with(Color.BG1, screen, frame)


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = HEIGHT

        result = sut.height

        assert result == expected


class TestWidth:
    def test_returns_content_width(
        self, sut, theme, renderer, screen, viewmodel, frame
    ) -> None:
        with patch(
            "prompt_toolkit.formatted_text.fragment_list_width", return_value=42
        ), patch(
            "prompt_toolkit.formatted_text.split_lines", return_value=[("foo", "bar")]
        ):
            expected = 42 + (2 * HORIZONTAL_PADDING)

            result = sut.width

            assert result == expected
