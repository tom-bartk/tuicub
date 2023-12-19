from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import Tileset
from ..state import GameScreenState


@frozen
class UpdateRackAction(Action):
    """An intent to update the player's rack.

    Attributes:
        rack (Tileset): The new rack of the player.
    """

    rack: Tileset


class UpdateRackReducer(Reducer[UpdateRackAction, GameScreenState]):
    """The reducer for the update rack action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[UpdateRackAction]:
        return UpdateRackAction

    def apply(self, action: UpdateRackAction, state: GameScreenState) -> GameScreenState:
        """Apply the update rack action.

        Updates the rack to the one from the action.

        Args:
            action (UpdateRackAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, rack=action.rack)
