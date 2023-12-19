from httperactor import HttpMethod, Request

from ...common.models import GameState
from ..state import GameScreenState
from .base import BaseGameRequestInteractor, GameRequest


class RedoRequest(GameRequest):
    """The request for redoing a move.

    Request documentation: https://docs.tuicub.com/api/#/Games/redo
    """

    __slots__ = ()

    @property
    def game_path(self) -> str:
        return "/moves"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.PATCH


class RedoRequestInteractor(BaseGameRequestInteractor):
    """The interactor for sending the redo request."""

    __slots__ = ()

    def create_request(self, game_id: str, state: GameScreenState) -> Request[GameState]:
        return RedoRequest(game_id=game_id)
