from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from httperactor import HttpMethod, Request
from marshmallow_generic import GenericSchema
from pydepot import Action, Store

from ...common.http import BaseHttpInteractor, BaseRequest
from ...common.models import GameState
from ...common.schemas import GameStateSchema
from ..errors import NoCurrentGameError
from ..state import GameScreenState


class GameRequest(BaseRequest[GameState], ABC):
    """Base class for game requests."""

    __slots__ = ("_game_id",)

    def __init__(self, game_id: str):
        """Initialize new game request.

        Args:
            game_id (str): The id of the game.
        """
        self._game_id: str = game_id

    @property
    @abstractmethod
    def game_path(self) -> str:
        """The part of the URL path after '/games/{game_id}'."""

    @property
    def response_schema(self) -> GenericSchema[GameState]:
        return GameStateSchema()

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.POST

    @property
    def path(self) -> str:
        return f"/games/{self._game_id}{self.game_path}"


class BaseGameRequestInteractor(BaseHttpInteractor[GameState], ABC):
    """Base interactor for game requests."""

    __slots__ = ("_local_store",)

    def __init__(
        self, local_store: Store[GameScreenState], *args: Any, **kwargs: Any
    ) -> None:
        self._local_store: Store[GameScreenState] = local_store
        super().__init__(*args, **kwargs)

    @abstractmethod
    def create_request(self, game_id: str, state: GameScreenState) -> Request[GameState]:
        """Create a game request.

        Returns a new game request based on the game id and the current game screen state.

        Args:
            game_id (str): The game id.
            state (GameScreenState): The current state of the game screen.

        Returns:
            The game request.
        """

    @property
    def request(self) -> Request[GameState]:
        if self.store.state.current_game:
            return self.create_request(
                game_id=self.store.state.current_game.id, state=self._local_store.state
            )
        raise NoCurrentGameError()

    def actions(self, response: GameState) -> Sequence[Action]:
        return []
