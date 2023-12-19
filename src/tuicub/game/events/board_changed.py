from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ..actions import UpdateBoardAction
from ..models import Board, Tile, Tileset
from .base import GameEventHandler


@frozen
class BoardChangedEvent(Event):
    """Event `board_changed` sent when tiles on the board change.

    The board can change when a player plays any tiles, undos or redos a move,
    or the player that currently has a turn disconnects.

    Attributes:
        board (list[list[int]]): The current state of the board represented as a list of
            lists of tiles.
        new_tiles (list[int]): The list of new tiles that have been played this turn.
    """

    board: list[list[int]]
    new_tiles: list[int]


class BoardChangedEventHandler(GameEventHandler[BoardChangedEvent]):
    """Handler for the board changed event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[BoardChangedEvent]:
        return BoardChangedEvent

    def actions(self, event: BoardChangedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the board changed event.

        Dispatches an `UpdateBoardAction` with the new board and a new list
        of recently played tiles.

        Args:
            event (BoardChangedEvent): The board changed event.

        Returns:
            A list of actions to dispatch.
        """
        tilesets = frozenset(Tileset.from_tile_ids(tiles=tiles) for tiles in event.board)
        new_tiles = frozenset(Tile.from_id(tile) for tile in event.new_tiles)

        return [UpdateBoardAction(board=Board(tilesets=tilesets), new_tiles=new_tiles)]


class BoardChangedEventSchema(GenericSchema[BoardChangedEvent]):
    board = fields.List(fields.List(fields.Int()))
    new_tiles = fields.List(fields.Int())
