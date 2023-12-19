from unittest.mock import create_autospec

import pytest
from prompt_toolkit.layout import Dimension
from prompt_toolkit.layout.controls import BufferControl

from src.tuicub.common.views import TextfieldView, TextfieldViewDelegate
from src.tuicub.common.views.textfield import TEXTFIELD_HEIGHT


@pytest.fixture()
def delegate() -> TextfieldViewDelegate:
    return create_autospec(TextfieldViewDelegate)


@pytest.fixture()
def sut(theme) -> TextfieldView:
    return TextfieldView(theme=theme)


class TestPreferredHeight:
    def test_returns_exact_textfield_height(self, sut) -> None:
        expected = Dimension.exact(TEXTFIELD_HEIGHT)

        result = sut.preferred_height(width=13, max_available_height=42)

        assert result.min == expected.min
        assert result.max == expected.max
        assert result.preferred == expected.preferred


class TestReset:
    def test_resets_buffer_control(self, sut) -> None:
        buffer_control = create_autospec(BufferControl)
        sut.buffer_control = buffer_control

        sut.reset()

        buffer_control.reset.assert_called_once()


class TestGetChildren:
    def test_returns_input_container(self, sut) -> None:
        expected = [sut.input_container]

        result = sut.get_children()

        assert result == expected


class TestFocusTarget:
    def test_returns_buffer_control(self, sut) -> None:
        expected = sut.buffer_control

        result = sut.focus_target()

        assert result == expected


class TestOnTextChanged:
    def test_when_delegate_set__calls_on_text_changed_on_delegate_with_buffer_text(
        self, sut, delegate
    ) -> None:
        sut.buffer.text = "foo"

        sut.set_delegate(delegate)
        sut.buffer.on_text_changed()

        delegate.on_text_changed.assert_called_once_with("foo")
