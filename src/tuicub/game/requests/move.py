from httperactor import Request

from ...common.models import GameState
from ..actions import ResetStateAction
from ..models import Tileset
from ..state import GameScreenState
from .base import BaseGameRequestInteractor, GameRequest


class MoveRequest(GameRequest):
    """The request for moving tiles.

    Request documentation: https://docs.tuicub.com/api/#/Games/move
    """

    __slots__ = ("_board",)

    def __init__(self, game_id: str, board: list[list[int]]):
        super().__init__(game_id=game_id)
        self._board: list[list[int]] = board

    @property
    def game_path(self) -> str:
        return "/moves"

    @property
    def body(self) -> list | dict | None:
        return {"board": self._board}


class MoveRequestInteractor(BaseGameRequestInteractor):
    """The interactor for sending the move request."""

    __slots__ = ()

    def create_request(self, game_id: str, state: GameScreenState) -> Request[GameState]:
        """Creates a move request.

        The board of the request is calculated by removing all selected tiles
        from their tilesets and merging them with the currently highlighted tileset.

        Args:
            game_id (str): The id of the game.
            state (GameScreenState): The current state of the game screen.

        Returns:
            The move request.
        """
        selected_tile_ids: frozenset[int] = frozenset(
            tile.id for tile in state.selected_tiles
        )
        highlighted_tileset: Tileset = state.highlighted_tileset or Tileset()

        not_highlighted_tilesets: frozenset[Tileset] = frozenset(
            tileset for tileset in state.board.tilesets if tileset != highlighted_tileset
        )

        board: set[frozenset[int]] = set()
        for tileset in not_highlighted_tilesets:
            board.add(
                frozenset(
                    tile.id for tile in tileset.tiles if tile.id not in selected_tile_ids
                )
            )

        highlighted_tile_ids: frozenset[int] = frozenset(
            tile.id for tile in highlighted_tileset.tiles
        )
        board.add(selected_tile_ids.union(highlighted_tile_ids))

        return MoveRequest(
            game_id=game_id, board=[list(tileset) for tileset in board if tileset]
        )

    async def side_effects(self, response: GameState) -> None:
        """Side effects to perform for the move tiles response.

        Dispatches a `ResetStateAction` to the local store.

        Args:
            response (GameState): The new game state after moving tiles.
        """
        self._local_store.dispatch(ResetStateAction())
