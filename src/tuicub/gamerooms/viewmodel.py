from __future__ import annotations

from collections.abc import Sequence
from functools import singledispatchmethod
from typing import TypeVar

from prompt_toolkit import application
from pydepot import Store

from ..common.state import State
from .state import GameroomsState, SetGameroomsRowsAction
from .view import GameroomRowViewModel

TState = TypeVar("TState", GameroomsState, State)


class GameroomsViewModel:
    """The viewmodel of the gamerooms view."""

    __slots__ = ("_is_list_empty", "_local_store", "_store", "__weakref__")

    def __init__(self, store: Store[State], local_store: Store[GameroomsState]):
        self._store: Store[State] = store
        self._local_store: Store[GameroomsState] = local_store
        self._is_list_empty: bool = False

    def is_list_empty(self) -> bool:
        """Returns True if the list is empty, False otherwise."""
        return self._is_list_empty

    def rows(self) -> Sequence[GameroomRowViewModel]:
        """Returns viewmodels of list rows."""
        return self._local_store.state.rows

    @singledispatchmethod
    def on_state(self, state: TState) -> None:
        """The hook of the store subscriber."""

    @on_state.register
    def _(self, state: State) -> None:
        self._is_list_empty = state.gamerooms is not None and len(state.gamerooms) == 0
        self._local_store.dispatch(SetGameroomsRowsAction(state.gamerooms or ()))
        application.get_app().invalidate()

    @on_state.register
    def _(self, state: GameroomsState) -> None:
        application.get_app().invalidate()

    def subscribe(self) -> None:
        self._store.subscribe(self, include_current=True)  # type: ignore
        self._local_store.subscribe(self, include_current=True)  # type: ignore

    def unsubscribe(self) -> None:
        self._store.unsubscribe(self)  # type: ignore[arg-type]
        self._local_store.unsubscribe(self)  # type: ignore[arg-type]
