from httperactor import Request

from ...common.models import GameState
from ..state import GameScreenState
from .base import BaseGameRequestInteractor, GameRequest


class EndTurnRequest(GameRequest):
    """The request for ending a turn.

    Request documentation: https://docs.tuicub.com/api/#/Games/end_turn
    """

    __slots__ = ()

    @property
    def game_path(self) -> str:
        return "/turns/end"


class EndTurnRequestInteractor(BaseGameRequestInteractor):
    """The interactor for sending the end turn request."""

    __slots__ = ()

    def create_request(self, game_id: str, state: GameScreenState) -> Request[GameState]:
        return EndTurnRequest(game_id=game_id)
