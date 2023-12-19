from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event

from ..actions.end_turn import EndTurnAction
from .base import GameEventHandler


@frozen
class TurnEndedEvent(Event):
    """Event `turn_ended` sent when a turn of a player ends.

    Turn ends when a player chooses to end it after playing at least one tile, or
    after drawing a tile.
    """


class TurnEndedEventHandler(GameEventHandler[TurnEndedEvent]):
    """Handler for the turn ended event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[TurnEndedEvent]:
        return TurnEndedEvent

    def actions(self, event: TurnEndedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the turn ended event.

        Dispatches an `EndTurnAction`.

        Args:
            event (TurnEndedEvent): The turn ended event.

        Returns:
            A list of actions to dispatch.
        """
        return [EndTurnAction()]
