from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...common.models import Player
from ..state import GameScreenState


@frozen
class SetWinnerAction(Action):
    """An intent to set the winner.

    Attributes:
        winner (Player): The player that won the game.
    """

    winner: Player


class SetWinnerReducer(Reducer[SetWinnerAction, GameScreenState]):
    """The reducer for the set winner action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetWinnerAction]:
        return SetWinnerAction

    def apply(self, action: SetWinnerAction, state: GameScreenState) -> GameScreenState:
        """Apply the set winner action.

        Updates the winner to the one from the action.

        Args:
            action (SetWinnerAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, winner=action.winner)
