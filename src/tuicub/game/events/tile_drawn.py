from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ..actions import AddDrawnTileAction
from ..models import Tile
from .base import GameEventHandler


@frozen
class TileDrawnEvent(Event):
    """Event `tile_drawn` sent when a player draws a tile.

    Attributes:
        tile (int): The id of the drawn tile.
    """

    tile: int


class TileDrawnEventHandler(GameEventHandler[TileDrawnEvent]):
    """Handler for the tile drawn event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[TileDrawnEvent]:
        return TileDrawnEvent

    def actions(self, event: TileDrawnEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the tile drawn event.

        Dispatches an `AddDrawnTileAction` with the drawn tile.

        Args:
            event (TileDrawnEvent): The tile drawn event.

        Returns:
            A list of actions to dispatch.
        """
        return [AddDrawnTileAction(tile=Tile.from_id(event.tile))]


class TileDrawnEventSchema(GenericSchema[TileDrawnEvent]):
    tile = fields.Int()
