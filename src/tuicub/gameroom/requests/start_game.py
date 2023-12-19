from collections.abc import Sequence

from httperactor import HttpMethod, Request
from marshmallow_generic import GenericSchema
from pydepot import Action

from ...common.http import BaseHttpInteractor, BaseRequest
from ...common.models import Game, Gameroom
from ...common.schemas import GameSchema
from ...common.state import SetCurrentGameAction
from ...common.strings import GAMEROOM_START_GAME_CONFIRMATION
from ..exception import NoCurrentGameroomError


class StartGameRequest(BaseRequest[Game]):
    """The request for starting a game.

    Request documentation: https://docs.tuicub.com/api/#/Gamerooms/start_game
    """

    __slots__ = ("_gameroom",)

    def __init__(self, gameroom: Gameroom):
        self._gameroom: Gameroom = gameroom

    @property
    def path(self) -> str:
        return f"/gamerooms/{self._gameroom.id}/game"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.POST

    @property
    def response_schema(self) -> GenericSchema[Game]:
        return GameSchema()


class StartGameInteractor(BaseHttpInteractor[Game]):
    """The interactor for sending the start game request."""

    __slots__ = ()

    @property
    def request(self) -> Request[Game]:
        if self.store.state.current_gameroom:
            return StartGameRequest(gameroom=self.store.state.current_gameroom)
        raise NoCurrentGameroomError()

    @property
    def confirmation(self) -> str:
        return GAMEROOM_START_GAME_CONFIRMATION

    def actions(self, response: Game) -> Sequence[Action]:
        """Actions to dispatch for the start game response.

        Dispatches a `SetCurrentGameAction` with the started game.

        Args:
            response (Game): The started game.

        Returns:
            A list of actions to dispatch.
        """
        return [SetCurrentGameAction(game=response)]
