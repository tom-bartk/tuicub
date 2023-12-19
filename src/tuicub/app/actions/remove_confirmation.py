from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..state import AppState


@frozen
class RemoveConfirmationAction(Action):
    """An intent to unset the current confirmation.

    Attributes:
        result (bool): The result of the confirmation.
    """

    result: bool


class RemoveConfirmationReducer(Reducer[RemoveConfirmationAction, AppState]):
    """The reducer for the remove confirmation action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[RemoveConfirmationAction]:
        return RemoveConfirmationAction

    def apply(self, action: RemoveConfirmationAction, state: AppState) -> AppState:
        """Apply the remove confirmation action.

        Sets the confirmation to None.

        Args:
            action (RemoveConfirmationAction): The action to apply.
            state (AppState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, confirmation=None)
