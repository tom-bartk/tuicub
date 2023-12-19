from pydepot import Store

from ...app.actions import RemoveConfirmationReducer, SetConfirmationReducer
from ...app.state import AppState
from ..module import CommonModule
from .actions import (
    AddGameroomUserReducer,
    DeleteGameroomReducer,
    FinishGameReducer,
    RemoveCurrentGameroomReducer,
    RemoveGameroomUserReducer,
    SetCurrentGameReducer,
    SetCurrentGameroomReducer,
    SetCurrentUserReducer,
    SetGameroomsReducer,
)
from .state import State
from .store import TuicubStore


class StateModule:
    __slots__ = ("_app_store", "_store")

    @property
    def app_store(self) -> Store[AppState]:
        return self._app_store

    @property
    def store(self) -> Store[State]:
        return self._store

    def __init__(self, common_module: CommonModule):
        self._store = TuicubStore(initial_state=State(), logger=common_module.logger)
        self._app_store = TuicubStore(
            initial_state=AppState(), logger=common_module.logger
        )
        self._register_global_reducers()
        self._register_app_reducers()

    def _register_global_reducers(self) -> None:
        self._store.register(AddGameroomUserReducer())
        self._store.register(DeleteGameroomReducer())
        self._store.register(FinishGameReducer())
        self._store.register(RemoveCurrentGameroomReducer())
        self._store.register(RemoveGameroomUserReducer())
        self._store.register(SetCurrentGameReducer())
        self._store.register(SetCurrentUserReducer())
        self._store.register(SetCurrentGameroomReducer())
        self._store.register(SetGameroomsReducer())

    def _register_app_reducers(self) -> None:
        self._app_store.register(SetConfirmationReducer())
        self._app_store.register(RemoveConfirmationReducer())
