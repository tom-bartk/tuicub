from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ..actions import UpdatePileCountAction
from .base import GameEventHandler


@frozen
class PileCountChangedEvent(Event):
    """Event `pile_count_changed` sent when the number of tiles on the pile changes.

    Pile count changes when a player draws a tile, or a player disconnects and their
    rack is shuffled back to the pile.

    Attributes:
        pile_count (int): The current number of tiles on the pile.
    """

    pile_count: int


class PileCountChangedEventHandler(GameEventHandler[PileCountChangedEvent]):
    """Handler for the pile count changed event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[PileCountChangedEvent]:
        return PileCountChangedEvent

    def actions(self, event: PileCountChangedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the pile count changed event.

        Dispatches an `UpdatePileCountAction` with the pile count from the event.

        Args:
            event (PileCountChangedEvent): The pile count changed event.

        Returns:
            A list of actions to dispatch.
        """
        return [UpdatePileCountAction(pile_count=event.pile_count)]


class PileCountChangedEventSchema(GenericSchema[PileCountChangedEvent]):
    pile_count = fields.Int()
