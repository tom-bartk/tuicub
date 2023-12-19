from collections.abc import Sequence

from httperactor import HttpMethod, Request
from marshmallow_generic import GenericSchema
from pydepot import Action

from ...common.http import BaseHttpInteractor, BaseRequest
from ...common.models import Gameroom
from ...common.schemas import GameroomSchema
from ...common.state import SetCurrentGameroomAction


class CreateGameroomRequest(BaseRequest[Gameroom]):
    """The request for creating a gameroom.

    Request documentation: https://docs.tuicub.com/api/#/Gamerooms/create_gameroom
    """

    __slots__ = ()

    @property
    def path(self) -> str:
        return "/gamerooms"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.POST

    @property
    def response_schema(self) -> GenericSchema[Gameroom]:
        return GameroomSchema()


class CreateGameroomInteractor(BaseHttpInteractor[Gameroom]):
    """The interactor for sending the create gameroom request."""

    __slots__ = ()

    @property
    def request(self) -> Request[Gameroom]:
        return CreateGameroomRequest()

    def actions(self, response: Gameroom) -> Sequence[Action]:
        """Actions to dispatch for the create gameroom response.

        Dispatches a `SetCurrentGameroomAction` with the created gameroom.

        Args:
            response (Gameroom): The created gameroom.

        Returns:
            A list of actions to dispatch.
        """
        return [SetCurrentGameroomAction(gameroom=response)]
