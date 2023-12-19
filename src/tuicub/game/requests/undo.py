from httperactor import HttpMethod, Request

from ...common.models import GameState
from ..state import GameScreenState
from .base import BaseGameRequestInteractor, GameRequest


class UndoRequest(GameRequest):
    """The request for undoing a move.

    Request documentation: https://docs.tuicub.com/api/#/Games/undo
    """

    __slots__ = ()

    @property
    def game_path(self) -> str:
        return "/moves"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.DELETE


class UndoRequestInteractor(BaseGameRequestInteractor):
    """The interactor for sending the undo request."""

    __slots__ = ()

    def create_request(self, game_id: str, state: GameScreenState) -> Request[GameState]:
        return UndoRequest(game_id=game_id)
