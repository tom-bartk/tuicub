from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...common.confirmation.confirmation import Confirmation
from ..state import AppState


@frozen
class SetConfirmationAction(Action):
    """An intent to set the current confirmation.

    Attributes:
        confirmation (Confirmation): The confirmation to set.
    """

    confirmation: Confirmation


class SetConfirmationReducer(Reducer[SetConfirmationAction, AppState]):
    """The reducer for the set confirmation action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetConfirmationAction]:
        return SetConfirmationAction

    def apply(self, action: SetConfirmationAction, state: AppState) -> AppState:
        """Apply the set confirmation action.

        Sets the current confirmation.

        Args:
            action (SetConfirmationAction): The action to apply.
            state (AppState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, confirmation=action.confirmation)
