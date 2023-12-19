from asockit import SocketReader, SocketWriter
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyPressEvent

from ..confirmation.service import ConfirmationService
from ..models import Keybind
from ..strings import EXIT_CONFIRMATION, EXIT_KEYBIND_TOOLTIP


class ExitService:
    """A service for exiting the `prompt_toolkit.Application`."""

    __slots__ = ("_confirmation_service", "_socket_reader", "_socket_writer", "_keybind")

    @property
    def keybind(self) -> Keybind:
        """The keybind ("q") for quitting the application."""
        return self._keybind

    def __init__(
        self,
        confirmation_service: ConfirmationService,
        socket_reader: SocketReader,
        socket_writer: SocketWriter,
    ):
        """Initialize new instance.

        Args:
            confirmation_service (ConfirmationService): The confirmation service.
            socket_reader (SocketReader): The events listener.
            socket_writer (SocketWriter): The events client.
        """
        self._confirmation_service: ConfirmationService = confirmation_service
        self._socket_reader: SocketReader = socket_reader
        self._socket_writer: SocketWriter = socket_writer
        self._keybind: Keybind = Keybind(
            key="q", display_key="q", tooltip=EXIT_KEYBIND_TOOLTIP, action=self.exit_app
        )

    async def exit_app(self, event: KeyPressEvent) -> None:
        """Exits the application after successful confirmation.

        Args:
            event (KeyPressEvent): The event that triggered this coroutine.
        """
        confirmed = await self._confirmation_service.confirm(EXIT_CONFIRMATION)
        if confirmed:
            await self._exit(app=event.app)

    async def force_exit(self, event: KeyPressEvent) -> None:
        """Exits the application without confirmation.

        Args:
            event (KeyPressEvent): The event that triggered this coroutine.
        """
        await self._exit(app=event.app)

    async def _exit(self, app: Application) -> None:
        await self._socket_reader.stop()
        await self._socket_writer.close()
        app.exit()
