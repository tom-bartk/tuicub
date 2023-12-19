from typing import Any

from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ...common.models import Alert, AlertType, Player
from ...common.schemas import PlayerSchema
from ...common.services.alert_service import AlertService
from ...common.strings import GAME_PLAYER_LEFT_ALERT
from .base import GameEventHandler


@frozen
class PlayerLeftEvent(Event):
    """Event `player_left` sent when a player leaves the game.

    Attributes:
        player (Player): The player that left the game.
    """

    player: Player


class PlayerLeftEventHandler(GameEventHandler[PlayerLeftEvent]):
    """Handler for the player left event."""

    __slots__ = ("_alert_service",)

    @property
    def event_type(self) -> type[PlayerLeftEvent]:
        return PlayerLeftEvent

    def __init__(self, alert_service: AlertService, *args: Any, **kwargs: Any):
        self._alert_service: AlertService = alert_service
        super().__init__(*args, **kwargs)

    def side_effects(self, event: PlayerLeftEvent) -> None:
        """Side effects to perform for the player left event.

        Queues an info alert notifying that a player has left the game.

        Args:
            event (PlayerLeftEvent): The player left event.
        """
        self._alert_service.queue_alert(
            Alert(GAME_PLAYER_LEFT_ALERT.format(event.player.name), AlertType.INFO)
        )


class PlayerLeftEventSchema(GenericSchema[PlayerLeftEvent]):
    player = fields.Nested(PlayerSchema)
