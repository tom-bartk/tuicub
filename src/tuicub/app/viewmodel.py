from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TypeVar

from more_itertools import collapse, intersperse
from pydepot import Store

from ..common.models import Keybind
from ..common.state import State
from ..common.views import Color, Text, TextPart, text
from .state import AppState
from .status import StatusViewModel

TState = TypeVar("TState", AppState, State)


class AppViewModel:
    """The viewmodel for the app view."""

    __slots__ = (
        "_local_store",
        "_global_keybinds",
        "_keybinds",
        "_status_viewmodel",
        "__weakref__",
    )

    def __init__(
        self,
        local_store: Store[AppState],
        global_keybinds: Sequence[Keybind],
        status_viewmodel: StatusViewModel,
    ):
        self._local_store: Store[AppState] = local_store
        self._global_keybinds: Sequence[Keybind] = global_keybinds
        self._keybinds: Callable[[], Sequence[Keybind]] = lambda: []
        self._status_viewmodel: StatusViewModel = status_viewmodel

    def keybinds(self) -> Text:
        """Returns the text representation of all currently active keybinds."""
        active_keybinds = tuple(
            keybind
            for keybind in self._keybinds()
            if keybind.condition() and not keybind.is_hidden
        )
        return keybinds_text(
            (*self._global_keybinds, *active_keybinds),
            enabled=self._local_store.state.confirmation is None,
        )

    def on_state(self, state: AppState) -> None:
        self._status_viewmodel.set_confirmation(confirmation=state.confirmation)

    def subscribe(self) -> None:
        self._local_store.subscribe(self, include_current=True)

    def unsubscribe(self) -> None:
        self._local_store.unsubscribe(self)

    def bind_keybinds(self, keybinds: Callable[[], Sequence[Keybind]]) -> None:
        self._keybinds = keybinds


def keybinds_text(keybinds: tuple[Keybind, ...], enabled: bool) -> Text:
    return Text(
        *collapse(
            intersperse(
                TextPart(" Ⅰ", Color.BG7 if enabled else Color.BG5),
                tuple(
                    (
                        *text.keybind(
                            kb.display_key,
                            key_color=Color.YELLOW if enabled else Color.YELLOW_DIM,
                            brackets_color=Color.BG7 if enabled else Color.BG5,
                        ),
                        TextPart(
                            kb.tooltip or "", fg=Color.FG1 if enabled else Color.FG5
                        ),
                    )
                    for kb in keybinds
                ),
            )
        )
    )
