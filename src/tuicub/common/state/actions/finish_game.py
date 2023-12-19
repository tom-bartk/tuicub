from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import remove_gameroom
from ..state import State


@frozen
class FinishGameAction(Action):
    """An intent to finish currently played game."""


class FinishGameReducer(Reducer[FinishGameAction, State]):
    """The reducer for the finish game action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[FinishGameAction]:
        return FinishGameAction

    def apply(self, action: FinishGameAction, state: State) -> State:
        """Apply the finish game action.

        Removes the current gameroom from the list of gamerooms,
        and sets both the current gameroom and the current game to `None`.

        Args:
            action (FinishGameAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        current_gameroom_id: str | None = (
            state.current_gameroom.id if state.current_gameroom else None
        )
        gamerooms = remove_gameroom(
            gameroom_id=current_gameroom_id, gamerooms=state.gamerooms
        )

        return evolve(
            state, current_gameroom=None, current_game=None, gamerooms=gamerooms
        )
