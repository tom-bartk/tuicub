from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import SelectionMode, Tileset
from ..state import GameScreenState


@frozen
class SetTilesSelectionAction(Action):
    """An intent to set the selection mode to tiles."""


class SetTilesSelectionReducer(Reducer[SetTilesSelectionAction, GameScreenState]):
    """The reducer for the set tiles selection action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetTilesSelectionAction]:
        return SetTilesSelectionAction

    def apply(
        self, action: SetTilesSelectionAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the set tiles selection action.

        Updates the selection mode to tiles, and resets the virtual tileset.

        Args:
            action (SetTilesSelectionAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(
            state, selection_mode=SelectionMode.TILES, virtual_tileset=Tileset()
        )
