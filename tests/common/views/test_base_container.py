from typing import Any
from unittest.mock import Mock, create_autospec

import pytest
from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import Container, Dimension
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.renderer import Screen, WritePosition

from src.tuicub.common.views.base_container import BaseContainer, BasicContainer
from src.tuicub.common.views.renderer import Renderer


@pytest.fixture()
def screen() -> Screen:
    return create_autospec(Screen)


@pytest.fixture()
def mouse_handlers() -> MouseHandlers:
    return create_autospec(MouseHandlers)


@pytest.fixture()
def key_bindings() -> KeyBindingsBase:
    return create_autospec(KeyBindingsBase)


@pytest.fixture()
def parent_style() -> str:
    return "foo"


class MockBaseContainer(BaseContainer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.mock_render = Mock()
        super().__init__(*args, **kwargs)

    def render(
        self, renderer: Renderer, write_position: WritePosition, parent_style: str
    ) -> None:
        self.mock_render(
            renderer=renderer, write_position=write_position, parent_style=parent_style
        )


class TestBaseContainer:
    @pytest.fixture()
    def sut(self, key_bindings) -> MockBaseContainer:
        return MockBaseContainer(key_bindings=key_bindings)

    def test_preferred_height__returns_max_available_height(
        self, sut: MockBaseContainer
    ) -> None:
        expected = Dimension(preferred=42)

        result = sut.preferred_height(width=100, max_available_height=42)

        assert result.preferred == expected.preferred
        assert result.min == expected.min
        assert result.max == expected.max

    def test_preferred_width__returns_max_available_width(
        self, sut: MockBaseContainer
    ) -> None:
        expected = Dimension(preferred=42)

        result = sut.preferred_width(max_available_width=42)

        assert result.preferred == expected.preferred
        assert result.min == expected.min
        assert result.max == expected.max

    def test_write_to_screen__renders_with_renderer_write_position_and_parent_style(
        self, sut: MockBaseContainer, screen, mouse_handlers
    ) -> None:
        write_position = Mock()

        sut.write_to_screen(
            screen=screen,
            mouse_handlers=mouse_handlers,
            write_position=write_position,
            parent_style="foo",
            erase_bg=False,
            z_index=None,
        )

        sut.mock_render.assert_called_once_with(
            renderer=Renderer(
                screen=screen, parent_style="foo", mouse_handlers=mouse_handlers
            ),
            write_position=write_position,
            parent_style="foo",
        )

    def test_get_key_bindings__returns_key_bindings_from_init(
        self, sut: MockBaseContainer, key_bindings
    ) -> None:
        expected = key_bindings

        result = sut.get_key_bindings()

        assert result == expected

    def test_get_children__returns_empty_list(self, sut: MockBaseContainer) -> None:
        expected: list[Container] = []

        result = sut.get_children()

        assert result == expected


class MockBasicContainer(BasicContainer):
    def reset(self) -> None:
        pass

    def write_to_screen(
        self,
        screen: Screen,
        mouse_handlers: MouseHandlers,
        write_position: WritePosition,
        parent_style: str,
        erase_bg: bool,
        z_index: int | None,
    ) -> None:
        pass


class TestBasicContainer:
    @pytest.fixture()
    def sut(self) -> MockBasicContainer:
        return MockBasicContainer()

    def test_preferred_height__returns_empty_dimension(
        self, sut: MockBasicContainer
    ) -> None:
        expected = Dimension()

        result = sut.preferred_height(width=100, max_available_height=42)

        assert result.preferred == expected.preferred
        assert result.min == expected.min
        assert result.max == expected.max

    def test_preferred_width__returns_empty_dimension(
        self, sut: MockBasicContainer
    ) -> None:
        expected = Dimension()

        result = sut.preferred_width(max_available_width=42)

        assert result.preferred == expected.preferred
        assert result.min == expected.min
        assert result.max == expected.max

    def test_get_children__returns_empty_list(self, sut: MockBasicContainer) -> None:
        expected: list[Container] = []

        result = sut.get_children()

        assert result == expected
