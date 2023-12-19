from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...models import Game
from ..state import State


@frozen
class SetCurrentGameAction(Action):
    """An intent to set the current game.

    Attributes:
        game (Game): The game to set.
    """

    game: Game


class SetCurrentGameReducer(Reducer[SetCurrentGameAction, State]):
    """The reducer for the set current game action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetCurrentGameAction]:
        return SetCurrentGameAction

    def apply(self, action: SetCurrentGameAction, state: State) -> State:
        """Apply the set current game action.

        Sets the current game to the one from the action.

        Args:
            action (SetCurrentGameAction): The action to apply.
            state (State): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, current_game=action.game)
