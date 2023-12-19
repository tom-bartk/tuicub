from httperactor import Request

from ...common.models import GameState
from ..state import GameScreenState
from .base import BaseGameRequestInteractor, GameRequest


class DrawRequest(GameRequest):
    """The request for drawing a tile.

    Request documentation: https://docs.tuicub.com/api/#/Games/draw
    """

    __slots__ = ()

    @property
    def game_path(self) -> str:
        return "/turns/draw"


class DrawRequestInteractor(BaseGameRequestInteractor):
    """The interactor for sending the draw request."""

    __slots__ = ()

    def create_request(self, game_id: str, state: GameScreenState) -> Request[GameState]:
        return DrawRequest(game_id=game_id)
