from prompt_toolkit.layout.screen import Screen

from src.tuicub.game.widgets.base import BaseWidget
from src.tuicub.game.widgets.frame import Frame
from src.tuicub.game.widgets.renderer import Renderer


class MockWidget(BaseWidget):
    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        pass


class TestWidth:
    def test_returns_zero(self) -> None:
        sut = MockWidget()
        expected = 0

        result = sut.width

        assert result == expected


class TestHeight:
    def test_returns_zero(self) -> None:
        sut = MockWidget()
        expected = 0

        result = sut.height

        assert result == expected
