from unittest.mock import Mock, create_autospec

import pytest
from prompt_toolkit.layout import Container, Dimension

from src.tuicub.common.views import HCenterView


@pytest.fixture()
def content() -> Container:
    return create_autospec(Container)


@pytest.fixture()
def sut(content) -> HCenterView:
    return HCenterView(content=content, content_width=42)


class TestPreferredHeight:
    def test_returns_content_preferred_height(self, sut, content) -> None:
        content.preferred_height = Mock(return_value=Dimension.exact(13))
        expected = Dimension.exact(13)

        result = sut.preferred_height(width=50, max_available_height=100)

        assert result.min == expected.min
        assert result.max == expected.max
        assert result.preferred == expected.preferred


class TestReset:
    def test_resets_content(self, sut, content) -> None:
        sut.reset()

        content.reset.assert_called_once()
