from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import Tile
from ..state import GameScreenState


@frozen
class SetHighlightedTileAction(Action):
    """An intent to set a highlighted tile.

    Attributes:
        tile (Tile): The tile to highlight.
    """

    tile: Tile


class SetHighlightedTileReducer(Reducer[SetHighlightedTileAction, GameScreenState]):
    """The reducer for the set highlighted tile action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetHighlightedTileAction]:
        return SetHighlightedTileAction

    def apply(
        self, action: SetHighlightedTileAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the set highlighted tile action.

        Updates the highlighted tile to the one from the action.

        Args:
            action (SetHighlightedTileAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, highlighted_tile=action.tile)
