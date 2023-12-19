from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import SelectionMode, Tileset
from ..state import GameScreenState


@frozen
class EndTurnAction(Action):
    """An intent to end the player's turn."""


class EndTurnReducer(Reducer[EndTurnAction, GameScreenState]):
    """The reducer for the end turn action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[EndTurnAction]:
        return EndTurnAction

    def apply(self, action: EndTurnAction, state: GameScreenState) -> GameScreenState:
        """Apply the end turn action.

        Unsets higlighted tile and tileset, and resets selected tiles and virtual tileset.

        Args:
            action (EndTurnAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(
            state,
            highlighted_tile=None,
            highlighted_tileset=None,
            selection_mode=SelectionMode.TILES,
            selected_tiles=frozenset(),
            virtual_tileset=Tileset(),
        )
