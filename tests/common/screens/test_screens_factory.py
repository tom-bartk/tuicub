from unittest.mock import Mock

import pytest

from src.tuicub.common.screens import ScreensFactory


@pytest.fixture()
def sut() -> ScreensFactory:
    return ScreensFactory()


class TestCreate:
    def test_when_factory_added_for_screen_name__returns_result_of_factory(
        self, sut
    ) -> None:
        screen = Mock()
        factory = Mock(return_value=screen)
        expected = screen

        sut.add_factory("foo", factory=factory)
        result = sut.create(screen_name="foo")

        assert result == expected

    def test_when_factory_not_added_for_screen_name__raises_not_implemented_error(
        self, sut
    ) -> None:
        with pytest.raises(NotImplementedError):
            sut.create(screen_name="foo")
