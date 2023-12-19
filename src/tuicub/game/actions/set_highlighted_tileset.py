from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import Tileset
from ..state import GameScreenState


@frozen
class SetHighlightedTilesetAction(Action):
    """An intent to set a highlighted tileset.

    Attributes:
        tileset (Tileset): The tileset to highlight.
    """

    tileset: Tileset


class SetHighlightedTilesetReducer(Reducer[SetHighlightedTilesetAction, GameScreenState]):
    """The reducer for the set highlighted tileset action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[SetHighlightedTilesetAction]:
        return SetHighlightedTilesetAction

    def apply(
        self, action: SetHighlightedTilesetAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the set highlighted tileset action.

        Updates the highlighted tileset to the one from the action.

        Args:
            action (SetHighlightedTilesetAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, highlighted_tileset=action.tileset)
