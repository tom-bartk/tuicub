from unittest.mock import Mock, create_autospec

import pytest
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.renderer import Screen

from src.tuicub.common.views.renderer import Renderer


@pytest.fixture()
def screen() -> Screen:
    return create_autospec(Screen)


@pytest.fixture()
def mouse_handlers() -> MouseHandlers:
    return create_autospec(MouseHandlers)


@pytest.fixture()
def parent_style() -> str:
    return "foo"


@pytest.fixture()
def sut(screen, mouse_handlers, parent_style) -> Renderer:
    return Renderer(
        screen=screen, parent_style=parent_style, mouse_handlers=mouse_handlers
    )


class TestRender:
    def test_when_style_none__writes_container_to_screen_using_parent_style(
        self, sut, mouse_handlers, screen, parent_style
    ) -> None:
        container = Mock()
        write_position = Mock()

        sut.render(container=container, write_position=write_position, style=None)

        container.write_to_screen.assert_called_once_with(
            screen=screen,
            mouse_handlers=mouse_handlers,
            write_position=write_position,
            parent_style=parent_style,
            erase_bg=False,
            z_index=None,
        )

    def test_when_style_not_none__writes_container_to_screen_using_style(
        self, sut, mouse_handlers, screen
    ) -> None:
        container = Mock()
        write_position = Mock()
        style = "bar"

        sut.render(container=container, write_position=write_position, style=style)

        container.write_to_screen.assert_called_once_with(
            screen=screen,
            mouse_handlers=mouse_handlers,
            write_position=write_position,
            parent_style=style,
            erase_bg=False,
            z_index=None,
        )
