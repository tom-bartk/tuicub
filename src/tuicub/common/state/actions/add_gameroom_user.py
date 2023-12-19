from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import User
from ..state import State


@frozen
class AddGameroomUserAction(Action):
    """An intent to add a user to the current gameroom's users list.

    Attributes:
        user (User): The user to add.
    """

    user: User


class AddGameroomUserReducer(Reducer[AddGameroomUserAction, State]):
    """The reducer for the add gameroom user action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[AddGameroomUserAction]:
        return AddGameroomUserAction

    def apply(self, action: AddGameroomUserAction, state: State) -> State:
        """Apply the add gameroom user action.

        If the current gameroom is not None, and the user is not already
        in the gameroom, then the user is appended to the gameroom's list of users.

        Args:
            action (AddGameroomUserAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        if state.current_gameroom and action.user not in state.current_gameroom.users:
            gameroom = evolve(
                state.current_gameroom,
                users=(*state.current_gameroom.users, action.user),
            )
            return evolve(state, current_gameroom=gameroom)

        return state
