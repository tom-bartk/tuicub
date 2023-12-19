from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import SelectionMode, VirtualTileset
from ..state import GameScreenState


@frozen
class SetTilesetsSelectionAction(Action):
    """An intent to set the selection mode to tilesets."""


class SetTilesetsSelectionReducer(Reducer[SetTilesetsSelectionAction, GameScreenState]):
    """The reducer for the set tilesets selection action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetTilesetsSelectionAction]:
        return SetTilesetsSelectionAction

    def apply(
        self, action: SetTilesetsSelectionAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the set tilesets selection action.

        Updates the selection mode to tilesets, sets the virtual tileset to a new one made
        from selected tiles, and updates the highlighted tileset to the virtual tileset.

        Args:
            action (SetTilesetsSelectionAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        virtual_tileset = VirtualTileset(tiles=tuple(state.selected_tiles))
        return evolve(
            state,
            selection_mode=SelectionMode.TILESETS,
            virtual_tileset=virtual_tileset,
            highlighted_tileset=virtual_tileset,
        )
