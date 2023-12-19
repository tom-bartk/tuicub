from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..state import State


@frozen
class RemoveCurrentGameroomAction(Action):
    """An intent to unset the current gameroom."""


class RemoveCurrentGameroomReducer(Reducer[RemoveCurrentGameroomAction, State]):
    """The reducer for the remove current gameroom action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[RemoveCurrentGameroomAction]:
        return RemoveCurrentGameroomAction

    def apply(self, action: RemoveCurrentGameroomAction, state: State) -> State:
        """Apply the remove current gameroom action.

        Sets the current gameroom to `None` without deleting it from
        the list of gamerooms.

        Args:
            action (RemoveCurrentGameroomAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, current_gameroom=None)
