from typing import Generic, TypeVar

from eventoolkit import Event, StoreEventHandler

from ..state import GameScreenState

TEvent = TypeVar("TEvent", bound=Event)


class GameEventHandler(Generic[TEvent], StoreEventHandler[TEvent, GameScreenState]):
    """Base handler for game events."""

    __slots__ = ("__weakref__",)
