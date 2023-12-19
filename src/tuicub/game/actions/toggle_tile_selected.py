from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import Tile
from ..state import GameScreenState


@frozen
class ToggleTileSelectedAction(Action):
    """An intent to toggle the selection state of the currently highlighted tile."""


class ToggleTileSelectedReducer(Reducer[ToggleTileSelectedAction, GameScreenState]):
    """The reducer for toggle tile selected action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[ToggleTileSelectedAction]:
        return ToggleTileSelectedAction

    def apply(
        self, action: ToggleTileSelectedAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the toggle tile selected action.

        If the currently highlighted tile is already selected,
        then it's removed from the selected tiles. Otherwise, the tile
        is added to the selected tiles.

        Args:
            action (ToggleTileSelectedAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        if highlighted_tile := state.highlighted_tile:
            selected_tiles: frozenset[Tile] = state.selected_tiles
            if highlighted_tile in selected_tiles:
                return evolve(
                    state, selected_tiles=selected_tiles.difference([highlighted_tile])
                )
            else:
                return evolve(
                    state, selected_tiles=selected_tiles.union([highlighted_tile])
                )
        return state
