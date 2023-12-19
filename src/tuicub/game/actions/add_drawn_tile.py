from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import Tile
from ..state import GameScreenState


@frozen
class AddDrawnTileAction(Action):
    """An intent to add the drawn tile to the player's rack.

    Attributes:
        tile (Tile): The drawn tile.
    """

    tile: Tile


class AddDrawnTileReducer(Reducer[AddDrawnTileAction, GameScreenState]):
    """The reducer for the add drawn tile action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[AddDrawnTileAction]:
        return AddDrawnTileAction

    def apply(
        self, action: AddDrawnTileAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the add drawn tile action.

        Sets new tiles to a set containing just the drawn tile.

        Args:
            action (AddDrawnTileAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, new_tiles=frozenset({action.tile}))
