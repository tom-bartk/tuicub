from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import Gameroom, remove_gameroom
from ..state import State


@frozen
class DeleteGameroomAction(Action):
    """An intent to delete a gameroom from the list of gamerooms.

    Attributes:
        gameroom (Gameroom): The gameroom to delete.
    """

    gameroom: Gameroom


class DeleteGameroomReducer(Reducer[DeleteGameroomAction, State]):
    """The reducer for the delete gameroom action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[DeleteGameroomAction]:
        return DeleteGameroomAction

    def apply(self, action: DeleteGameroomAction, state: State) -> State:
        """Apply the delete gameroom action.

        Removes the gameroom from the list of gamerooms. If the deleted gameroom
        is also the current gameroom, then the current gameroom is set to `None`.

        Args:
            action (DeleteGameroomAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        gamerooms = remove_gameroom(
            gameroom_id=action.gameroom.id, gamerooms=state.gamerooms
        )

        current_gameroom: Gameroom | None = state.current_gameroom
        if current_gameroom and current_gameroom.id == action.gameroom.id:
            current_gameroom = None

        return evolve(state, gamerooms=gamerooms, current_gameroom=current_gameroom)
