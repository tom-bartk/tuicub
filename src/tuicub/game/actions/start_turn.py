from attrs import evolve, frozen
from more_itertools import first
from pydepot import Action, Reducer

from ..models import SelectionMode, Tileset
from ..state import GameScreenState


@frozen
class StartTurnAction(Action):
    """An intent to start the player's turn."""


class StartTurnReducer(Reducer[StartTurnAction, GameScreenState]):
    """The reducer for the start turn action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[StartTurnAction]:
        return StartTurnAction

    def apply(self, action: StartTurnAction, state: GameScreenState) -> GameScreenState:
        """Apply the start turn action.

        Sets the highlighted tile to the first one from rack, unsets the highlighted
        tileset, resets selected and new tiles, resets the virtual tileset,
        and sets the selection mode to tiles.

        Args:
            action (StartTurnAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(
            state,
            highlighted_tile=first(state.rack.tiles, None),
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
            new_tiles=frozenset(),
        )
