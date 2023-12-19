import pytest

from src.tuicub.common.confirmation import FutureConfirmation, FutureConfirmationFactory


@pytest.fixture()
def text() -> str:
    return "Are you sure?"


@pytest.fixture()
def sut(loop) -> FutureConfirmationFactory:
    return FutureConfirmationFactory(loop=loop)


class TestFutureConfirmation:
    def test_create__returns_future_confirmation(self, sut, text) -> None:
        result = sut.create(text=text)

        assert isinstance(result, FutureConfirmation)
        assert result.text == text

    def test_create__creates_future_using_loop(self, sut, loop) -> None:
        sut.create(text=text)

        loop.create_future.assert_called_once()
