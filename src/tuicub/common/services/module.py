import asyncio

from prompt_toolkit.output import Output

from ..confirmation.module import ConfirmationModule
from ..confirmation.service import ConfirmationService
from ..events.module import EventsModule
from ..state.module import StateModule
from .alert_service import AlertService
from .auth_service import AuthService
from .exit_service import ExitService
from .screen_size_service import ScreenSizeService


class ServicesModule:
    __slots__ = (
        "_alert_service",
        "_auth_service",
        "_confirmation_service",
        "_exit_service",
        "_screen_size_service",
    )

    @property
    def alert_service(self) -> AlertService:
        return self._alert_service

    @property
    def auth_service(self) -> AuthService:
        return self._auth_service

    @property
    def confirmation_service(self) -> ConfirmationService:
        return self._confirmation_service

    @property
    def exit_service(self) -> ExitService:
        return self._exit_service

    @property
    def screen_size_service(self) -> ScreenSizeService:
        return self._screen_size_service

    def __init__(
        self,
        confirmation_module: ConfirmationModule,
        events_module: EventsModule,
        state_module: StateModule,
        output: Output,
    ):
        self._alert_service = AlertService()
        self._auth_service = AuthService()
        self._confirmation_service = ConfirmationService(
            confirmation_factory=confirmation_module.factory,
            store=state_module.app_store,
            lock=asyncio.Lock(),
        )
        self._exit_service = ExitService(
            confirmation_service=self._confirmation_service,
            socket_reader=events_module.socket_reader,
            socket_writer=events_module.socket_writer,
        )
        self._screen_size_service = ScreenSizeService(
            output=output,
        )
