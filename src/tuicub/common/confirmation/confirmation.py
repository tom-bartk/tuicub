import asyncio
from abc import ABC, abstractmethod

from ..views import Color, Text, TextPart, text


class Confirmation(ABC):
    """Base class for a confirmation."""

    __slots__ = ()

    @property
    def ui_text(self) -> Text:
        """Returns the confirmation text formatted for displaying."""
        return Text(
            TextPart(f" {self.text} ", fg=Color.FG0, bold=True),
            *text.keybind("y"),
            TextPart("/", Color.FG4),
            *text.keybind("n"),
        )

    @property
    @abstractmethod
    def text(self) -> str:
        """The text of the confirmation."""

    @abstractmethod
    def answer(self, answer: bool) -> None:
        """Answer the confirmation.

        Args:
            answer (bool): Whether the confirmation is rejected, or confirmed.
        """

    @abstractmethod
    async def result(self) -> bool:
        """Coroutine that waits for user to answer the confirmation.

        Returns:
            Whether the confrimation was confirmed, or rejected.
        """


class FutureConfirmation(Confirmation):
    """A confirmation that uses the `asyncio.Future`."""

    __slots__ = ("_text", "_fut")

    @property
    def text(self) -> str:
        return self._text

    def __init__(self, text: str, fut: asyncio.Future[bool]):
        """Initialize new confirmation.

        Args:
            text (str): The text of the confirmation.
            fut (asyncio.Future[bool]): The future to use for delivering the answer.
        """
        self._text: str = text
        self._fut: asyncio.Future[bool] = fut

    def answer(self, answer: bool) -> None:
        self._fut.set_result(answer)

    async def result(self) -> bool:
        return await self._fut
