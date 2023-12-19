from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import Gameroom
from ..state import State


@frozen
class SetCurrentGameroomAction(Action):
    """An intent to set the current gameroom.

    Attributes:
        gameroom (Gameroom): The gameroom to set.
    """

    gameroom: Gameroom


class SetCurrentGameroomReducer(Reducer[SetCurrentGameroomAction, State]):
    """The reducer for the set current gameroom action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetCurrentGameroomAction]:
        return SetCurrentGameroomAction

    def apply(self, action: SetCurrentGameroomAction, state: State) -> State:
        """Apply the set current gameroom action.

        Sets the current gameroom to the one from the action.

        Args:
            action (SetCurrentGameroomAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, current_gameroom=action.gameroom)
