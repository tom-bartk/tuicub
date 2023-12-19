import asyncio

from pydepot import Store

from ...app.actions import RemoveConfirmationAction, SetConfirmationAction
from ...app.state import AppState
from .factory import ConfirmationFactory


class ConfirmationService:
    """Service that handles the confirmation process."""

    __slots__ = ("_confirmation_factory", "_lock", "_store")

    def __init__(
        self,
        confirmation_factory: ConfirmationFactory,
        store: Store[AppState],
        lock: asyncio.Lock,
    ):
        """Initialize new service.

        Args:
            confirmation_factory (ConfirmationFactory): The factory of confirmations.
            store (Store[AppState]): The store of the app state.
            lock (asyncio.Lock): The lock to ensure only one confirmation at a time.
        """
        self._confirmation_factory: ConfirmationFactory = confirmation_factory
        self._store: Store[AppState] = store
        self._lock: asyncio.Lock = lock

    async def confirm(self, text: str) -> bool:
        """Show confirmation and wait for the answer.

        Creates a new confirmation and displays it on the screen, then waits
        for the answer and returns it.

        Args:
            text (str): The confirmation text to display.

        Returns:
            Whether the confirmation is confirmed, or rejected.
        """
        async with self._lock:
            confirmation = self._confirmation_factory.create(text=text)
            self._store.dispatch(SetConfirmationAction(confirmation))

            result = await confirmation.result()
            self._store.dispatch(RemoveConfirmationAction(result=result))

            return result
