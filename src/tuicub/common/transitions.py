from abc import ABC, abstractmethod

from pyllot import Transition, TransitionDirection

from .screens import ScreenName
from .state import State


class TransitionCondition(ABC):
    """Base class for a transition condition."""

    __slots__ = ()

    @abstractmethod
    def __call__(self, state: State) -> bool:
        """Call."""


class HasCurrentUser(TransitionCondition):
    """A condition that is true if the global state has a current user."""

    __slots__ = ()

    def __call__(self, state: State) -> bool:
        return state.current_user is not None


class HasCurrentGameroom(TransitionCondition):
    """A condition that is true if the global state has a current gameroom."""

    __slots__ = ()

    def __call__(self, state: State) -> bool:
        return state.current_gameroom is not None


class HasCurrentGame(TransitionCondition):
    """A condition that is true if the global state has a current game."""

    __slots__ = ()

    def __call__(self, state: State) -> bool:
        return state.current_game is not None


class HasNoCurrentGameroom(TransitionCondition):
    """A condition that is true if the global state has no current gameroom."""

    __slots__ = ()

    def __call__(self, state: State) -> bool:
        return state.current_gameroom is None


class HasNoCurrentGame(TransitionCondition):
    """A condition that is true if the global state has no current game."""

    __slots__ = ()

    def __call__(self, state: State) -> bool:
        return state.current_game is None


REGISTER_USER_TO_GAMEROOMS = Transition(
    source=ScreenName.REGISTER_USER,
    destination=ScreenName.GAMEROOMS,
    direction=TransitionDirection.PUSH,
    condition=HasCurrentUser(),
)
GAMEROOMS_TO_GAMEROOM = Transition(
    source=ScreenName.GAMEROOMS,
    destination=ScreenName.GAMEROOM,
    direction=TransitionDirection.PUSH,
    condition=HasCurrentGameroom(),
)
GAMEROOM_TO_GAME = Transition(
    source=ScreenName.GAMEROOM,
    destination=ScreenName.GAME,
    direction=TransitionDirection.PUSH,
    condition=HasCurrentGame(),
)
GAME_TO_GAMEROOMS: Transition[State] = Transition(
    source=ScreenName.GAME,
    destination=ScreenName.GAMEROOMS,
    direction=TransitionDirection.POP,
    condition=HasNoCurrentGame(),
)
GAMEROOM_TO_GAMEROOMS: Transition[State] = Transition(
    source=ScreenName.GAMEROOM,
    destination=ScreenName.GAMEROOMS,
    direction=TransitionDirection.POP,
    condition=HasNoCurrentGameroom(),
)
