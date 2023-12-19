from unittest.mock import Mock, create_autospec, patch

import pytest

from src.tuicub.game.viewmodels.player import PlayerViewModel
from src.tuicub.game.widgets.player import HEIGHT, PlayerWidget


@pytest.fixture()
def viewmodel() -> PlayerViewModel:
    return create_autospec(PlayerViewModel)


@pytest.fixture()
def sut(viewmodel, theme) -> PlayerWidget:
    return PlayerWidget(viewmodel=viewmodel, theme=theme)


class TestRender:
    def test_writes_viewmodel_content(
        self, sut, theme, renderer, screen, viewmodel, frame
    ) -> None:
        content = Mock()
        viewmodel.content.return_value = content

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.write_content.assert_called_once_with(content, frame, screen)
        viewmodel.content.assert_called_once_with(theme=theme)


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = HEIGHT

        result = sut.height

        assert result == expected


class TestWidth:
    def test_returns_content_width(
        self, sut, theme, renderer, screen, viewmodel, frame
    ) -> None:
        with patch("prompt_toolkit.formatted_text.fragment_list_width", return_value=42):
            expected = 42

            result = sut.width

            assert result == expected
