from collections.abc import Sequence

from httperactor import Request
from marshmallow_generic import GenericSchema
from pydepot import Action

from ...common.http import BaseHttpInteractor, BaseRequest
from ...common.models import Gameroom
from ...common.schemas import GameroomSchema
from ...common.state import SetGameroomsAction


class GetGameroomsRequest(BaseRequest[Sequence[Gameroom]]):
    """The request for getting active gamerooms.

    Request documentation: https://docs.tuicub.com/api/#/Gamerooms/get_gamerooms
    """

    __slots__ = ()

    @property
    def path(self) -> str:
        return "/gamerooms"

    @property
    def returns_list(self) -> bool:
        return True

    @property
    def response_schema(self) -> GenericSchema[Sequence[Gameroom]]:
        return GameroomSchema()  # type: ignore


class GetGameroomsInteractor(BaseHttpInteractor[Sequence[Gameroom]]):
    """The interactor for sending the get gamerooms request."""

    __slots__ = ()

    @property
    def request(self) -> Request[Sequence[Gameroom]]:
        return GetGameroomsRequest()

    def actions(self, response: Sequence[Gameroom]) -> Sequence[Action]:
        """Actions to dispatch for the get gamerooms response.

        Dispatches a `SetGameroomsAction` with the returned gamerooms.

        Args:
            response (Sequence[Gameroom]): The list of active gamerooms.

        Returns:
            A list of actions to dispatch.
        """
        return [SetGameroomsAction(gamerooms=response)]
