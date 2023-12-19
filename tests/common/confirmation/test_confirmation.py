import asyncio
from unittest.mock import AsyncMock, create_autospec

import pytest

from src.tuicub.common.confirmation import Confirmation, FutureConfirmation
from src.tuicub.common.views import Color, Text, TextPart


@pytest.fixture()
def text() -> str:
    return "Are you sure?"


@pytest.fixture()
def future() -> asyncio.Future[bool]:
    return create_autospec(asyncio.Future)


@pytest.fixture()
def sut(text, future) -> FutureConfirmation:
    return FutureConfirmation(text=text, fut=future)


class TestFutureConfirmation:
    def test_answer__sets_future_result_to_answer(self, sut, text, future) -> None:
        sut = FutureConfirmation(text=text, fut=future)
        expected = True

        sut.answer(answer=expected)

        future.set_result.assert_called_once_with(expected)

    @pytest.mark.asyncio()
    async def test_result__returns_awaited_future(self, sut, text) -> None:
        expected = True
        fut = AsyncMock(return_value=expected)()
        sut = FutureConfirmation(text=text, fut=fut)

        result = await sut.result()

        assert result == expected

    def test_text__returns_text_from_init(self, sut, text) -> None:
        expected = text

        result = sut.text

        assert result == expected


class MockConfirmation(Confirmation):
    @property
    def text(self) -> str:
        return "foo"

    def answer(self, answer: bool) -> None:
        pass

    async def result(self) -> bool:
        return True


class TestConfirmation:
    def test_ui_text__returns_text_with_yes_no_keybinds_text_parts(self) -> None:
        expected = Text(
            TextPart(" foo ", fg=Color.FG0, bold=True),
            TextPart("❬", fg=Color.BG8),
            TextPart("y", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG8),
            TextPart("/", Color.FG4),
            TextPart("❬", fg=Color.BG8),
            TextPart("n", fg=Color.YELLOW, bold=True),
            TextPart("❭", fg=Color.BG8),
        )
        sut = MockConfirmation()

        result = sut.ui_text

        assert result == expected
