from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ...common.models import Player
from ...common.schemas import PlayerSchema
from ..actions import UpdatePlayersAction
from .base import GameEventHandler


@frozen
class PlayersChangedEvent(Event):
    """Event `players_changed` sent when anything about the players change.

    That includes the list of players itself, the number of tiles in the rack of each
    player, or the current turn state.

    Attributes:
        players (list[Player]): The updated list of players.
    """

    players: list[Player]


class PlayersChangedEventHandler(GameEventHandler[PlayersChangedEvent]):
    """Handler for the players changed event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[PlayersChangedEvent]:
        return PlayersChangedEvent

    def actions(self, event: PlayersChangedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the players changed event.

        Dispatches an `UpdatePlayersAction` with the updated players.

        Args:
            event (PlayersChangedEvent): The players changed event.

        Returns:
            A list of actions to dispatch.
        """
        return [UpdatePlayersAction(players=tuple(event.players))]


class PlayersChangedEventSchema(GenericSchema[PlayersChangedEvent]):
    players = fields.List(fields.Nested(PlayerSchema))
