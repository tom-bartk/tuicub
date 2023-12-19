from __future__ import annotations

from attrs import field, frozen
from more_itertools import first

from ..common.models import Game, GameState, Player
from .models import Board, SelectionMode, Tile, Tileset


@frozen
class GameScreenState:
    """The local state of the game screen.

    Attributes:
        pile_count (int): The current number of tiles left to draw from.
        selection_mode (SelectionMode): The current selection mode.
        highlighted_tile (Tile | None): The currently highlighted tile.
        highlighted_tileset (Tileset | None): The currenly highlighted tileset.
        selected_tiles (frozenset[Tile]): All currently selected tiles.
        new_tiles (frozenset[Tile]): All tiles that were drawn or played this round.
        players (tuple[Player, ...]): The current list of players.
        winner (Player | None): An optional winner of the game.
        board (Board): The current board.
        rack (Tileset): The rack of the current user.
        virtual_tileset (Tileset): The
    """

    pile_count: int = field(default=0)
    selection_mode: SelectionMode = field(default=SelectionMode.TILES)

    highlighted_tile: Tile | None = field(default=None)
    highlighted_tileset: Tileset | None = field(default=None)

    selected_tiles: frozenset[Tile] = field(default=frozenset())
    new_tiles: frozenset[Tile] = field(default=frozenset())

    players: tuple[Player, ...] = field(default=())
    winner: Player | None = field(default=None)

    board: Board = field(default=Board())
    rack: Tileset = field(default=Tileset())
    virtual_tileset: Tileset = field(default=Tileset())

    @classmethod
    def from_game(cls, user_id: str, game: Game) -> GameScreenState:
        game_state: GameState = game.game_state
        tilesets = frozenset(
            [Tileset.from_tile_ids(tiles=tiles) for tiles in game_state.board]
        )

        board = Board(tilesets=tilesets)
        rack = Tileset.from_tile_ids(tiles=game_state.rack)
        player: Player = next(
            player for player in game_state.players if player.user_id == user_id
        )
        highlighted_tile = first(rack.tiles, None) if player.has_turn else None
        return GameScreenState(
            pile_count=game_state.pile_count,
            players=tuple(game_state.players),
            board=board,
            rack=rack,
            highlighted_tile=highlighted_tile,
        )
