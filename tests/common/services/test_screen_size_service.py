from unittest.mock import create_autospec

import pytest
from prompt_toolkit.renderer import Output, Size

from src.tuicub.common.services.screen_size_service import ScreenSizeService


@pytest.fixture()
def output() -> Output:
    return create_autospec(Output)


@pytest.fixture()
def sut(output) -> ScreenSizeService:
    return ScreenSizeService(output=output)


class TestWidth:
    def test_returns_number_of_columns_of_output_size(self, sut, output) -> None:
        size = create_autospec(Size)
        size.columns = 42
        output.get_size.return_value = size
        expected = 42

        result = sut.width()

        assert result == expected
