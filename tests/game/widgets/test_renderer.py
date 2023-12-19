from collections import defaultdict
from collections.abc import Callable
from unittest.mock import Mock, create_autospec

import pytest
from prompt_toolkit.layout.screen import _CHAR_CACHE, Char, Screen, Transparent

from src.tuicub.common.strings import BOTTOM_BORDER, TOP_BORDER
from src.tuicub.common.views import Color
from src.tuicub.game.widgets.base import BaseWidget
from src.tuicub.game.widgets.frame import Frame
from src.tuicub.game.widgets.renderer import (
    HorizontalPosition,
    Position,
    Renderer,
    SeparatorSide,
    Side,
    VerticalPosition,
)


@pytest.fixture()
def widget() -> Callable[[int, int], BaseWidget]:
    def factory(width: int = 10, height: int = 10) -> BaseWidget:
        _widget = Mock()
        _widget.width = width
        _widget.height = height
        _widget.render = Mock()
        return _widget

    return factory


@pytest.fixture()
def screen() -> Screen:
    screen = Mock()
    default_char2 = _CHAR_CACHE[" ", Transparent]
    screen.data_buffer = defaultdict(lambda: defaultdict(lambda: default_char2))
    screen.fill_area = Mock()
    return screen


@pytest.fixture()
def frame() -> Frame:
    return create_autospec(Frame)


@pytest.fixture()
def sut(theme) -> Renderer:
    return Renderer(theme=theme)


class TestWriteContent:
    def test_when_single_line__screen_data_buffer_has_one_dict(self, sut, screen) -> None:
        expected = {
            0: {
                0: Char("b", style="foo"),
                1: Char("a", style="foo"),
                2: Char("r", style="foo"),
            },
        }

        sut.write_content(
            [("foo", "bar")],
            frame=Frame(x=0, y=0, width=80, height=24),
            screen=screen,
        )

        assert screen.data_buffer == expected

    def test_when_two_lines__screen_data_buffer_has_two_dicts(self, sut, screen) -> None:
        expected = {
            0: {
                0: Char("b", style="foo"),
                1: Char("a", style="foo"),
                2: Char("r", style="foo"),
            },
            1: {
                0: Char("b", style="foo"),
                1: Char("a", style="foo"),
                2: Char("z", style="foo"),
            },
        }

        sut.write_content(
            [("foo", "bar\nbaz")],
            frame=Frame(x=0, y=0, width=80, height=24),
            screen=screen,
        )

        assert screen.data_buffer == expected


class TestWriteCenteredContent:
    def test_when_single_line__screen_data_buffer_has_single_dict_with_correct_offset(
        self, sut, screen
    ) -> None:
        expected = {
            0: {
                3: Char("b", style="foo"),
                4: Char("a", style="foo"),
                5: Char("r", style="foo"),
                6: Char("r", style="foo"),
            },
        }

        sut.write_centered_content(
            [("foo", "barr")],
            frame=Frame(x=0, y=0, width=10, height=24),
            screen=screen,
        )

        assert screen.data_buffer == expected

    def test_when_two_lines__screen_data_buffer_has_two_dicts_with_correct_offsets(
        self, sut, screen
    ) -> None:
        expected = {
            0: {
                3: Char("b", style="foo"),
                4: Char("a", style="foo"),
                5: Char("r", style="foo"),
                6: Char("r", style="foo"),
            },
            1: {
                4: Char("b", style="foo"),
                5: Char("z", style="foo"),
            },
        }

        sut.write_centered_content(
            [("foo", "barr\nbz")],
            frame=Frame(x=0, y=0, width=10, height=24),
            screen=screen,
        )

        assert screen.data_buffer == expected


class TestDrawBorder:
    def test_screen_data_buffer_contains_bordered_square(
        self, sut, screen, theme
    ) -> None:
        theme.to_framework_fg.return_value = "foo"
        expected = {
            0: {
                0: Char("┏", style="foo"),
                1: Char("━", style="foo"),
                2: Char("━", style="foo"),
                3: Char("┓", style="foo"),
            },
            1: {
                0: Char("┃", style="foo"),
                3: Char("┃", style="foo"),
            },
            2: {
                0: Char("┃", style="foo"),
                3: Char("┃", style="foo"),
            },
            3: {
                0: Char("┗", style="foo"),
                1: Char("━", style="foo"),
                2: Char("━", style="foo"),
                3: Char("┛", style="foo"),
            },
        }

        sut.draw_border(frame=Frame(x=0, y=0, width=4, height=4), screen=screen)

        assert screen.data_buffer == expected


class TestDrawSeparator:
    def test_when_side_top__draws_separator_on_first_line(
        self, sut, screen, theme
    ) -> None:
        theme.to_framework_fg.return_value = "foo"
        expected = {
            0: {
                0: Char(TOP_BORDER, style="foo"),
                1: Char(TOP_BORDER, style="foo"),
                2: Char(TOP_BORDER, style="foo"),
            }
        }

        sut.draw_separator(
            side=SeparatorSide.TOP,
            frame=Frame(x=0, y=0, width=3, height=3),
            screen=screen,
        )

        assert screen.data_buffer == expected

    def test_when_side_bottom__draws_separator_on_last_line(
        self, sut, screen, theme
    ) -> None:
        theme.to_framework_fg.return_value = "foo"
        expected = {
            2: {
                0: Char(BOTTOM_BORDER, style="foo"),
                1: Char(BOTTOM_BORDER, style="foo"),
                2: Char(BOTTOM_BORDER, style="foo"),
            }
        }

        sut.draw_separator(
            side=SeparatorSide.BOTTOM,
            frame=Frame(x=0, y=0, width=3, height=3),
            screen=screen,
        )

        assert screen.data_buffer == expected


class TestSetBackgroundColor:
    def test_fills_screen_area_with_bg_color_at_frame_write_position(
        self, sut, screen, theme, frame
    ) -> None:
        write_position = Mock()
        background_color = Mock()
        theme.to_framework_bg.return_value = background_color
        frame.to_write_position.return_value = write_position

        sut.set_background_color(Color.BG2, screen=screen, frame=frame)

        screen.fill_area.assert_called_once_with(write_position, style=background_color)


class TestRenderHorizontally:
    def test_when_position_left__renders_widgets_from_left_to_right(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget_1 = widget(width=10, height=10)
        widget_2 = widget(width=10, height=10)
        widget_3 = widget(width=10, height=10)

        sut.render_horizontally(
            widgets=[widget_1, widget_2, widget_3],
            position=HorizontalPosition.LEFT,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget_1.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=0, width=10, height=10)
        )
        widget_2.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=10, y=0, width=10, height=10)
        )
        widget_3.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=20, y=0, width=10, height=10)
        )

    def test_when_position_center__renders_widgets_in_the_center(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget_1 = widget(width=10, height=10)
        widget_2 = widget(width=10, height=10)
        widget_3 = widget(width=10, height=10)

        sut.render_horizontally(
            widgets=[widget_1, widget_2, widget_3],
            position=HorizontalPosition.CENTER,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget_1.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=5, y=0, width=10, height=10)
        )
        widget_2.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=15, y=0, width=10, height=10)
        )
        widget_3.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=25, y=0, width=10, height=10)
        )


class TestRenderVertically:
    def test_when_position_top__renders_widgets_from_top_to_bottom(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget_1 = widget(width=10, height=10)
        widget_2 = widget(width=10, height=10)
        widget_3 = widget(width=10, height=10)

        sut.render_vertically(
            widgets=[widget_1, widget_2, widget_3],
            position=VerticalPosition.TOP,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget_1.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=0, width=10, height=10)
        )
        widget_2.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=10, width=10, height=10)
        )
        widget_3.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=20, width=10, height=10)
        )

    def test_when_position_center__renders_widgets_in_the_center(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget_1 = widget(width=10, height=10)
        widget_2 = widget(width=10, height=10)
        widget_3 = widget(width=10, height=10)

        sut.render_vertically(
            widgets=[widget_1, widget_2, widget_3],
            position=VerticalPosition.CENTER,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget_1.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=5, width=10, height=10)
        )
        widget_2.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=15, width=10, height=10)
        )
        widget_3.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=25, width=10, height=10)
        )


class TestRenderWidget:
    def test_when_position_top__side_left__renders_widget_at_top_left(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.TOP,
            side=Side.LEFT,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=0, width=10, height=10)
        )

    def test_when_position_bottom__side_left__renders_widget_at_bottom_left(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.BOTTOM,
            side=Side.LEFT,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=30, width=10, height=10)
        )

    def test_when_position_center__side_left__renders_widget_at_center_left(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.CENTER,
            side=Side.LEFT,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=0, y=15, width=10, height=10)
        )

    def test_when_position_top__side_center__renders_widget_at_top_center(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.TOP,
            side=Side.CENTER,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=15, y=0, width=10, height=10)
        )

    def test_when_position_bottom__side_center__renders_widget_at_bottom_center(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.BOTTOM,
            side=Side.CENTER,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=15, y=30, width=10, height=10)
        )

    def test_when_position_center__side_center__renders_widget_at_center_center(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.CENTER,
            side=Side.CENTER,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=15, y=15, width=10, height=10)
        )

    def test_when_position_top__side_right__renders_widget_at_top_right(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.TOP,
            side=Side.RIGHT,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=30, y=0, width=10, height=10)
        )

    def test_when_position_bottom__side_right__renders_widget_at_bottom_right(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.BOTTOM,
            side=Side.RIGHT,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=30, y=30, width=10, height=10)
        )

    def test_when_position_center__side_right__renders_widget_at_center_right(
        self, sut, screen, theme, frame, widget
    ) -> None:
        widget = widget(width=10, height=10)

        sut.render_widget(
            widget=widget,
            position=Position.CENTER,
            side=Side.RIGHT,
            frame=Frame(x=0, y=0, width=40, height=40),
            screen=screen,
        )

        widget.render.assert_called_once_with(
            renderer=sut, screen=screen, frame=Frame(x=30, y=15, width=10, height=10)
        )
