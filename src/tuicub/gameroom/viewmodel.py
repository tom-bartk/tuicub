from __future__ import annotations

from collections.abc import Sequence

from eventoolkit import EventsObserver
from prompt_toolkit import application
from pydepot import Store

from ..common.state import State
from ..common.views import Text, gameroom
from .view import UserRowViewModel


class GameroomViewModel:
    """The viewmodel of the gameroom view."""

    __slots__ = ("_events_observer", "_rows", "_store", "__weakref__")

    def __init__(self, store: Store[State], events_observer: EventsObserver):
        self._store: Store[State] = store
        self._events_observer = events_observer
        self._rows: Sequence[UserRowViewModel] = ()

    def rows(self) -> Sequence[UserRowViewModel]:
        """Returns viewmodels of the rows list."""
        return self._rows

    def gameroom_text(self) -> Text:
        """Returns the text of the gameroom header view."""
        if self._store.state.current_gameroom:
            return gameroom.gameroom_text(
                gameroom=self._store.state.current_gameroom,
                is_highlighted=False,
                horizontal_padding=0,
            )
        return Text()

    def on_state(self, state: State) -> None:
        users = state.current_gameroom.users if state.current_gameroom else ()
        owner_id = state.current_gameroom.owner_id if state.current_gameroom else None
        self._rows = tuple(
            UserRowViewModel(user, is_owner=user.id == owner_id) for user in users
        )

        application.get_app().invalidate()

    def subscribe(self) -> None:
        self._store.subscribe(self, include_current=True)
        self._events_observer.observe()

    def unsubscribe(self) -> None:
        self._store.unsubscribe(self)
        self._events_observer.stop()
