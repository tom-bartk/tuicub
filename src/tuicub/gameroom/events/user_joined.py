from collections.abc import Sequence

import pydepot
from attrs import frozen
from eventoolkit import Event
from marshmallow_generic import GenericSchema, fields

from ...common.events.handler import AlertingStoreEventHandler
from ...common.models import Alert, AlertType, User
from ...common.schemas import UserSchema
from ...common.state import AddGameroomUserAction
from ...common.strings import GAMEROOM_USER_JOINED_ALERT


@frozen
class UserJoinedEvent(Event):
    """Event `user_joined` sent when a user joins a gameroom.

    Attributes:
        user (User): The user that joined the gameroom.
    """

    user: User


class UserJoinedEventSchema(GenericSchema[UserJoinedEvent]):
    user = fields.Nested(UserSchema)


class UserJoinedEventHandler(AlertingStoreEventHandler[UserJoinedEvent]):
    """Handler for the user joined event."""

    __slots__ = "__weakref__"

    @property
    def event_type(self) -> type[UserJoinedEvent]:
        return UserJoinedEvent

    def actions(self, event: UserJoinedEvent) -> Sequence[pydepot.Action]:
        """Actions to dispatch for the user joined event.

        Dispatches a `AddGameroomUserAction` with the joining user.

        Args:
            event (UserJoinedEvent): The user joined event.

        Returns:
            A list of actions to dispatch.
        """
        return [AddGameroomUserAction(user=event.user)]

    def side_effects(self, event: UserJoinedEvent) -> None:
        """Side effects to perform for the user joined event.

        Queues an info alert notifying that a user has joined the gameroom.

        Args:
            event (UserJoinedEvent): The user joined event.
        """
        self._alert_service.queue_alert(
            Alert(GAMEROOM_USER_JOINED_ALERT.format(event.user.name), AlertType.INFO)
        )
