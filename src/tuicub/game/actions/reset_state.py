from attrs import evolve, frozen
from more_itertools import first
from pydepot import Action, Reducer

from ..models import SelectionMode, Tile, Tileset
from ..state import GameScreenState


@frozen
class ResetStateAction(Action):
    """An intent to reset the player's changes during a turn."""


class ResetStateReducer(Reducer[ResetStateAction, GameScreenState]):
    """The reducer for the reset state action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[ResetStateAction]:
        return ResetStateAction

    def apply(self, action: ResetStateAction, state: GameScreenState) -> GameScreenState:
        """Apply the reset state action.

        Unsets the highlighted tileset, sets the highlighted tile to the first from rack.
        Resets the selected tiles, virtual tileset and selection mode.

        Args:
            action (ResetStateAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(
            state,
            highlighted_tile=_get_highlighted_tile(state=state),
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
        )


def _get_highlighted_tile(state: GameScreenState) -> Tile | None:
    if state.rack.tiles:
        return first(state.rack.tiles, None)
    elif state.highlighted_tile:
        return state.highlighted_tile
    elif first_tileset := first(state.board.tilesets, None):
        return first(first_tileset.tiles, None)

    return None
