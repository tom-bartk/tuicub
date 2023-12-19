import asyncio

from ..state.module import StateModule
from .factory import ConfirmationFactory, FutureConfirmationFactory
from .interactor import ConfirmInteractor


class ConfirmationModule:
    __slots__ = ("_factory", "_interactor")

    @property
    def factory(self) -> ConfirmationFactory:
        return self._factory

    @property
    def interactor(self) -> ConfirmInteractor:
        return self._interactor

    def __init__(self, state_module: StateModule, loop: asyncio.AbstractEventLoop):
        self._factory = FutureConfirmationFactory(loop=loop)
        self._interactor: ConfirmInteractor = ConfirmInteractor(
            store=state_module.app_store
        )
