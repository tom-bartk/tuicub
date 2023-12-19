from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import User
from ..state import State


@frozen
class SetCurrentUserAction(Action):
    """An intent to set the current user.

    Attributes:
        user (User): The user to set.
    """

    user: User


class SetCurrentUserReducer(Reducer[SetCurrentUserAction, State]):
    """The reducer for the set current user action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetCurrentUserAction]:
        return SetCurrentUserAction

    def apply(self, action: SetCurrentUserAction, state: State) -> State:
        """Apply the set current user action.

        Sets the current user to the one from the action.

        Args:
            action (SetCurrentUserAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, current_user=action.user)
