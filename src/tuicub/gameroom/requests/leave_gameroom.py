from collections.abc import Sequence

from httperactor import HttpMethod, Request
from pydepot import Action

from ...common.http import BaseHttpInteractor, GameroomRequest
from ...common.models import Gameroom
from ...common.state import RemoveCurrentGameroomAction
from ...common.strings import GAMEROOM_LEAVE_GAMEROOM_CONFIRMATION
from ..exception import NoCurrentGameroomError


class LeaveGameroomRequest(GameroomRequest):
    """The request for leaving a gameroom.

    Request documentation: https://docs.tuicub.com/api/#/Gamerooms/leave_gameroom
    """

    __slots__ = ()

    @property
    def path(self) -> str:
        return f"/gamerooms/{self._gameroom.id}/users"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.DELETE


class LeaveGameroomInteractor(BaseHttpInteractor[Gameroom]):
    """The interactor for sending the leave gameroom request."""

    __slots__ = ()

    @property
    def request(self) -> Request[Gameroom]:
        if self.store.state.current_gameroom:
            return LeaveGameroomRequest(gameroom=self.store.state.current_gameroom)
        raise NoCurrentGameroomError()

    @property
    def confirmation(self) -> str:
        return GAMEROOM_LEAVE_GAMEROOM_CONFIRMATION

    def actions(self, response: Gameroom) -> Sequence[Action]:
        """Actions to dispatch for the leave gameroom response.

        Dispatches a `RemoveCurrentGameroomAction`.

        Args:
            response (Gameroom): The left gameroom.

        Returns:
            A list of actions to dispatch.
        """
        return [RemoveCurrentGameroomAction()]
