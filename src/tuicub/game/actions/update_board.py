from attrs import evolve, frozen
from pydepot import Action, Reducer

from ..models import Board, Tile
from ..state import GameScreenState


@frozen
class UpdateBoardAction(Action):
    """An intent to update the game board.

    Attributes:
        board (Board): The new board.
        new_tiles (frozenset[Tile]): Set of new tiles played this turn.
    """

    board: Board
    new_tiles: frozenset[Tile]


class UpdateBoardReducer(Reducer[UpdateBoardAction, GameScreenState]):
    """The reducer for the update board action."""

    __slots__ = ()

    @property
    def action_type(self) -> type[UpdateBoardAction]:
        return UpdateBoardAction

    def apply(self, action: UpdateBoardAction, state: GameScreenState) -> GameScreenState:
        """Apply the update board action.

        Updates the board to the one from the action, and sets the new tiles
        to those from the action plus those that currently are in the player's rack.

        Args:
            action (UpdateBoardAction): The action to apply.
            state (GameScreenState): The current state.

        Returns:
            The updated state.
        """
        new_tiles_from_rack = state.new_tiles.intersection(state.rack.tiles)
        return evolve(
            state,
            board=action.board,
            new_tiles=new_tiles_from_rack.union(action.new_tiles),
        )
