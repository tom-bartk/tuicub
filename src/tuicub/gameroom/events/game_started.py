from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ...common.events.handler import AlertingStoreEventHandler
from ...common.models import Alert, AlertType, Game
from ...common.schemas import GameSchema
from ...common.state import SetCurrentGameAction
from ...common.strings import GAME_STARTED_ALERT


@frozen
class GameStartedEvent(Event):
    """Event `game_started` sent when the gameroom's owner starts the game.

    Attributes:
        game (Game): The started game.
    """

    game: Game


class GameStartedEventSchema(GenericSchema[GameStartedEvent]):
    game = fields.Nested(GameSchema)


class GameStartedEventHandler(AlertingStoreEventHandler[GameStartedEvent]):
    """Handler for the game started event."""

    __slots__ = "__weakref__"

    @property
    def event_type(self) -> type[GameStartedEvent]:
        return GameStartedEvent

    def actions(self, event: GameStartedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the game started event.

        Dispatches a `SetCurrentGameAction` with the started game.

        Args:
            event (GameStartedEvent): The game started event.

        Returns:
            A list of actions to dispatch.
        """
        return [SetCurrentGameAction(game=event.game)]

    def side_effects(self, event: GameStartedEvent) -> None:
        """Side effects to perform for the game started event.

        Queues an info alert notifying that the game has started.

        Args:
            event (GameStartedEvent): The game started event.
        """
        self._alert_service.queue_alert(Alert(GAME_STARTED_ALERT, AlertType.INFO))
