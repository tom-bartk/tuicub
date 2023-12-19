import asyncio
from abc import ABC, abstractmethod

from .confirmation import Confirmation, FutureConfirmation


class ConfirmationFactory(ABC):
    """Base class for a confirmation factory."""

    __slots__ = ()

    @abstractmethod
    def create(self, text: str) -> Confirmation:
        """Create new confirmation.

        Args:
            text (str): The confirmation text to display.

        Returns:
            The created confirmation.
        """


class FutureConfirmationFactory(ConfirmationFactory):
    """A factory creating instances of `FutureConfirmation`."""

    __slots__ = ("_loop",)

    def __init__(self, loop: asyncio.AbstractEventLoop):
        """Initialize new factory.

        Args:
            loop (asyncio.AbstractEventLoop): The loop to use for creating new futures.
        """
        self._loop: asyncio.AbstractEventLoop = loop

    def create(self, text: str) -> Confirmation:
        return FutureConfirmation(text=text, fut=self._loop.create_future())
