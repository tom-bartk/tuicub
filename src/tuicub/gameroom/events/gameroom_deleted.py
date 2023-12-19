from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ...common.events.handler import AlertingStoreEventHandler
from ...common.models import Alert, AlertType, Gameroom
from ...common.schemas import GameroomSchema
from ...common.state import DeleteGameroomAction
from ...common.strings import GAMEROOM_DELETED_ALERT


@frozen
class GameroomDeletedEvent(Event):
    """Event `gameroom_deleted` sent when the gameroom's owner delets the gameroom.

    Attributes:
        gameroom (Gameroom): The deleted gameroom.
    """

    gameroom: Gameroom


class GameroomDeletedEventSchema(GenericSchema[GameroomDeletedEvent]):
    gameroom = fields.Nested(GameroomSchema)


class GameroomDeletedEventHandler(AlertingStoreEventHandler[GameroomDeletedEvent]):
    """Handler for the gameroom deleted event."""

    __slots__ = "__weakref__"

    @property
    def event_type(self) -> type[GameroomDeletedEvent]:
        return GameroomDeletedEvent

    def actions(self, event: GameroomDeletedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the gameroom deleted event.

        Dispatches a `DeleteGameroomAction` with the deleted gameroom.

        Args:
            event (GameroomDeletedEvent): The gameroom deleted event.

        Returns:
            A list of actions to dispatch.
        """
        return [DeleteGameroomAction(gameroom=event.gameroom)]

    def side_effects(self, event: GameroomDeletedEvent) -> None:
        """Side effects to perform for the gameroom deleted event.

        Queues an info alert notifying that the gameroom has been deleted.

        Args:
            event (GameroomDeletedEvent): The gameroom deleted event.
        """
        self._alert_service.queue_alert(Alert(GAMEROOM_DELETED_ALERT, AlertType.INFO))
