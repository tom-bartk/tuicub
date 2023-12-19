from collections.abc import Sequence

from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import Gameroom
from ..state import State


@frozen
class SetGameroomsAction(Action):
    """An intent to set gamerooms.

    Attributes:
        gamerooms (Sequence[Gameroom]): Gamerooms to set.
    """

    gamerooms: Sequence[Gameroom]


class SetGameroomsReducer(Reducer[SetGameroomsAction, State]):
    """The reducer for the set gamerooms action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetGameroomsAction]:
        return SetGameroomsAction

    def apply(self, action: SetGameroomsAction, state: State) -> State:
        """Apply the set gamerooms action.

        Sets gamerooms to ones from the action.

        Args:
            action (SetGameroomsAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, gamerooms=tuple(action.gamerooms))
