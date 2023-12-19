from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..state import GameScreenState


@frozen
class UpdatePileCountAction(Action):
    """An intent to update the pile count.

    Attributes:
        pile_count (int): The new pile count.
    """

    pile_count: int


class UpdatePileCountReducer(Reducer[UpdatePileCountAction, GameScreenState]):
    """The reducer for the update pile count action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[UpdatePileCountAction]:
        return UpdatePileCountAction

    def apply(
        self, action: UpdatePileCountAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the update pile count action.

        Updates the pile count to the one from the action.

        Args:
            action (UpdatePileCountAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, pile_count=action.pile_count)
