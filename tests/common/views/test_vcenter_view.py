from unittest.mock import Mock, create_autospec

import pytest
from prompt_toolkit.layout import Container, Dimension

from src.tuicub.common.views import VCenterView


@pytest.fixture()
def content() -> Container:
    return create_autospec(Container)


@pytest.fixture()
def sut(content) -> VCenterView:
    return VCenterView(content=content, content_height=42)


class TestPreferredWidth:
    def test_returns_content_preferred_width(self, sut, content) -> None:
        content.preferred_width = Mock(return_value=Dimension.exact(13))
        expected = Dimension.exact(13)

        result = sut.preferred_width(max_available_width=100)

        assert result.min == expected.min
        assert result.max == expected.max
        assert result.preferred == expected.preferred


class TestReset:
    def test_resets_content(self, sut, content) -> None:
        sut.reset()

        content.reset.assert_called_once()
