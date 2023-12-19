from collections.abc import Callable, Sequence
from unittest.mock import create_autospec

import pytest
from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import Container

from src.tuicub.common.views import ListView


@pytest.fixture()
def key_bindings() -> KeyBindingsBase:
    return create_autospec(KeyBindingsBase)


@pytest.fixture()
def rows() -> Sequence[Container]:
    return (create_autospec(Container), create_autospec(Container))


@pytest.fixture()
def header() -> Container:
    return create_autospec(Container)


@pytest.fixture()
def get_rows(rows) -> Callable[[], Sequence[Container]]:
    def wrapped() -> Sequence[Container]:
        return rows

    return wrapped


@pytest.fixture()
def sut(get_rows, key_bindings, header) -> ListView:
    return ListView(get_rows=get_rows, header=header, key_bindings=key_bindings)


class TestKeyBindigs:
    def test_returns_key_bindings_from_init(self, sut, key_bindings) -> None:
        expected = key_bindings

        result = sut.key_bindings

        assert result == expected


class TestGetContent:
    def test_returns_header_and_rows(self, sut, rows, header) -> None:
        expected = (header, *rows)

        result = sut.get_content()

        assert result == expected
