from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import User
from ..state import State


@frozen
class RemoveGameroomUserAction(Action):
    """An intent to remove a user from the current gameroom's users list.

    Attributes:
        user (User): The user to remove.
    """

    user: User


class RemoveGameroomUserReducer(Reducer[RemoveGameroomUserAction, State]):
    """The reducer for the remove gameroom user action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[RemoveGameroomUserAction]:
        return RemoveGameroomUserAction

    def apply(self, action: RemoveGameroomUserAction, state: State) -> State:
        """Apply the remove gameroom user action.

        If the current gameroom is not None, and the user is present in the gameroom,
        then the user is removed from the gameroom's list of users.

        Args:
            action (RemoveGameroomUserAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        if state.current_gameroom and action.user in state.current_gameroom.users:
            users = list(state.current_gameroom.users)
            users.remove(action.user)
            gameroom = evolve(state.current_gameroom, users=tuple(users))
            return evolve(state, current_gameroom=gameroom)

        return state
