from collections.abc import Sequence

from httperactor import HttpMethod, Request
from pydepot import Action

from ...common.http import BaseHttpInteractor, GameroomRequest
from ...common.models import Gameroom
from ...common.state import DeleteGameroomAction
from ...common.strings import GAMEROOM_DELETE_GAMEROOM_CONFIRMATION
from ..exception import NoCurrentGameroomError


class DeleteGameroomRequest(GameroomRequest):
    """The request for deleting a gameroom.

    Request documentation: https://docs.tuicub.com/api/#/Gamerooms/delete_gameroom
    """

    __slots__ = ()

    @property
    def path(self) -> str:
        return f"/gamerooms/{self._gameroom.id}"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.DELETE


class DeleteGameroomInteractor(BaseHttpInteractor[Gameroom]):
    """The interactor for sending the delete gameroom request."""

    __slots__ = ()

    @property
    def request(self) -> Request[Gameroom]:
        if self.store.state.current_gameroom:
            return DeleteGameroomRequest(gameroom=self.store.state.current_gameroom)
        raise NoCurrentGameroomError()

    @property
    def confirmation(self) -> str:
        return GAMEROOM_DELETE_GAMEROOM_CONFIRMATION

    def actions(self, response: Gameroom) -> Sequence[Action]:
        """Actions to dispatch for the delete gameroom response.

        Dispatches a `DeleteGameroomAction` with the deleted gameroom.

        Args:
            response (Gameroom): The deleted gameroom.

        Returns:
            A list of actions to dispatch.
        """
        return [DeleteGameroomAction(response)]
