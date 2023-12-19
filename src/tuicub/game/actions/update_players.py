from attrs import evolve, frozen
from pydepot import Action, Reducer

from ...common.models import Player
from ..state import GameScreenState


@frozen
class UpdatePlayersAction(Action):
    """An intent to update the list of players.

    Attributes:
        players (tuple[Player, ...]): The new list of players.
    """

    players: tuple[Player, ...]


class UpdatePlayersReducer(Reducer[UpdatePlayersAction, GameScreenState]):
    """The reducer for the update players action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[UpdatePlayersAction]:
        return UpdatePlayersAction

    def apply(
        self, action: UpdatePlayersAction, state: GameScreenState
    ) -> GameScreenState:
        """Apply the update players action.

        Updates players to those from the action.

        Args:
            action (UpdatePlayersAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        return evolve(state, players=action.players)
