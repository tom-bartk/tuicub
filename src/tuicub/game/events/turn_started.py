from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event

from ..actions.start_turn import StartTurnAction
from .base import GameEventHandler


@frozen
class TurnStartedEvent(Event):
    """Event `turn_started` sent when a turn of a player starts.

    Turn starts when another player ends their turn or disconnects.
    """


class TurnStartedEventHandler(GameEventHandler[TurnStartedEvent]):
    """Handler for the turn started event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[TurnStartedEvent]:
        return TurnStartedEvent

    def actions(self, event: TurnStartedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the turn started event.

        Dispatches a `StartTurnAction`.

        Args:
            event (TurnStartedEvent): The turn started event.

        Returns:
            A list of actions to dispatch.
        """
        return [StartTurnAction()]
