from collections.abc import Sequence
from typing import Any

from httperactor import HttpMethod, Request
from pydepot import Action, Store

from ...common.http import BaseHttpInteractor, GameroomRequest
from ...common.models import Gameroom
from ...common.state import SetCurrentGameroomAction
from ...common.strings import GAMEROOMS_GAMEROOM_NOT_SELECTED_ERROR
from ..state import GameroomsState


class JoinGameroomRequest(GameroomRequest):
    """The request for joining a gameroom.

    Request documentation: https://docs.tuicub.com/api/#/Gamerooms/join_gameroom
    """

    __slots__ = ()

    @property
    def path(self) -> str:
        return f"/gamerooms/{self._gameroom.id}/users"

    @property
    def method(self) -> HttpMethod:
        return HttpMethod.POST


class JoinGameroomInteractor(BaseHttpInteractor[Gameroom]):
    """The interactor for sending the join gameroom request."""

    __slots__ = ("_local_store",)

    def __init__(self, local_store: Store[GameroomsState], *args: Any, **kwargs: Any):
        """Initialize new interactor.

        Args:
            local_store (Store[GameroomsState]): The local screen store.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self._local_store: Store[GameroomsState] = local_store

    @property
    def request(self) -> Request[Gameroom]:
        index: int = self._local_store.state.selected_index
        gamerooms: tuple[Gameroom, ...] = self._store.state.gamerooms or ()
        if gamerooms and index < len(gamerooms):
            return JoinGameroomRequest(gameroom=gamerooms[index])

        raise GameroomNotSelectedError()

    def actions(self, response: Gameroom) -> Sequence[Action]:
        """Actions to dispatch for the join gameroom response.

        Dispatches a `SetCurrentGameroomAction` with the joined gameroom.

        Args:
            response (Gameroom): The joined gameroom.

        Returns:
            A list of actions to dispatch.
        """
        return [SetCurrentGameroomAction(gameroom=response)]


class GameroomNotSelectedError(ValueError):
    def __init__(self):
        super().__init__(GAMEROOMS_GAMEROOM_NOT_SELECTED_ERROR)
