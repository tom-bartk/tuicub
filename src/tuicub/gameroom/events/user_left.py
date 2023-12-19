from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ...common.events.handler import AlertingStoreEventHandler
from ...common.models import Alert, AlertType, User
from ...common.schemas import UserSchema
from ...common.state import RemoveGameroomUserAction
from ...common.strings import GAMEROOM_USER_LEFT_ALERT


@frozen
class UserLeftEvent(Event):
    """Event `user_left` sent when a user leaves a gameroom.

    Attributes:
        user: The user that left the gameroom.
    """

    user: User


class UserLeftEventSchema(GenericSchema[UserLeftEvent]):
    user = fields.Nested(UserSchema)


class UserLeftEventHandler(AlertingStoreEventHandler[UserLeftEvent]):
    """Handler for the user left event."""

    __slots__ = "__weakref__"

    @property
    def event_type(self) -> type[UserLeftEvent]:
        return UserLeftEvent

    def actions(self, event: UserLeftEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the user left event.

        Dispatches a `RemoveGameroomUserAction` with the leaving user.

        Args:
            event (UserLeftEvent): The user left event.

        Returns:
            A list of actions to dispatch.
        """
        return [RemoveGameroomUserAction(user=event.user)]

    def side_effects(self, event: UserLeftEvent) -> None:
        """Side effects to perform for the user left event.

        Queues an info alert notifying that a user has left the gameroom.

        Args:
            event (UserLeftEvent): The user left event.
        """
        self._alert_service.queue_alert(
            Alert(GAMEROOM_USER_LEFT_ALERT.format(event.user.name), AlertType.INFO)
        )
