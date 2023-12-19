from ...common import utils
from ..requests.draw import DrawRequestInteractor
from ..requests.end_turn import EndTurnRequestInteractor
from ..requests.move import MoveRequestInteractor
from ..requests.redo import RedoRequestInteractor
from ..requests.undo import UndoRequestInteractor


class ActionsInteractor:
    """Interactor that performs game actions."""

    __slots__ = (
        "_draw_interactor",
        "_end_turn_interactor",
        "_move_interactor",
        "_redo_interactor",
        "_undo_interactor",
    )

    def __init__(
        self,
        draw_interactor: DrawRequestInteractor,
        end_turn_interactor: EndTurnRequestInteractor,
        move_interactor: MoveRequestInteractor,
        redo_interactor: RedoRequestInteractor,
        undo_interactor: UndoRequestInteractor,
    ):
        self._draw_interactor: DrawRequestInteractor = draw_interactor
        self._end_turn_interactor: EndTurnRequestInteractor = end_turn_interactor
        self._move_interactor: MoveRequestInteractor = move_interactor
        self._redo_interactor: RedoRequestInteractor = redo_interactor
        self._undo_interactor: UndoRequestInteractor = undo_interactor

    def move_tiles(self) -> None:
        """Move tiles.

        Sends a move tiles requests.
        """
        utils.async_run(self._move_interactor.execute())

    def undo(self) -> None:
        """Undo a move.

        Sends an undo request.
        """
        utils.async_run(self._undo_interactor.execute())

    def redo(self) -> None:
        """Redo a move.

        Sends a redo request.
        """
        utils.async_run(self._redo_interactor.execute())

    def end_turn(self) -> None:
        """End the current turn.

        Sends an end turn request.
        """
        utils.async_run(self._end_turn_interactor.execute())

    def draw(self) -> None:
        """Draw a tile.

        Sends a draw tile request.
        """
        utils.async_run(self._draw_interactor.execute())
