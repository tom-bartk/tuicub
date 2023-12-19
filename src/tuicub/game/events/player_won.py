from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ...common.models import Player
from ...common.schemas import PlayerSchema
from ..actions import SetWinnerAction
from .base import GameEventHandler


@frozen
class PlayerWonEvent(Event):
    """Event `player_won` sent when a player wins the game.

    A player wins a game if they end a turn with no tiles left in their rack,
    or all other players disconnect.

    Attributes:
        winner (Player): The player that won the game.
    """

    winner: Player


class PlayerWonEventHandler(GameEventHandler[PlayerWonEvent]):
    """Handler for the player won event."""

    __slots__ = ()

    @property
    def event_type(self) -> type[PlayerWonEvent]:
        return PlayerWonEvent

    def actions(self, event: PlayerWonEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the player won event.

        Dispatches a `SetWinnerAction` with the winner.

        Args:
            event (PlayerWonEvent): The player won event.

        Returns:
            A list of actions to dispatch.
        """
        return [SetWinnerAction(winner=event.winner)]


class PlayerWonEventSchema(GenericSchema[PlayerWonEvent]):
    winner = fields.Nested(PlayerSchema)
