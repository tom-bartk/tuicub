from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ..actions import UpdateRackAction
from ..models import Tileset
from .base import GameEventHandler


@frozen
class RackChangedEvent(Event):
    """Event `rack_changed` sent when tiles in the player's rack change.

    Tiles in the rack can change when the player draws or play tiles.

    Attributes:
        rack (list[int]): The updated rack.
    """

    rack: list[int]


class RackChangedEventHandler(GameEventHandler[RackChangedEvent]):
    """Handler for the rack changed event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[RackChangedEvent]:
        return RackChangedEvent

    def actions(self, event: RackChangedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the rack changed event.

        Dispatches an `UpdateRackAction` with the new rack.

        Args:
            event (RackChangedEvent): The rack changed event.

        Returns:
            A list of actions to dispatch.
        """
        return [UpdateRackAction(rack=Tileset.from_tile_ids(tiles=event.rack))]


class RackChangedEventSchema(GenericSchema[RackChangedEvent]):
    rack = fields.List(fields.Int())
