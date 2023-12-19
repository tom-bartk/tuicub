from __future__ import annotations

from eventoolkit import EventsObserver
from prompt_toolkit import application
from pydepot import Store

from .models import SelectionMode, Tile, Tileset, VirtualTileset
from .services.board_service import BoardService
from .services.scroll_service import ScrollService
from .state import GameScreenState
from .viewmodels.pile import PileViewModel
from .viewmodels.player import PlayerViewModel
from .viewmodels.status_bar import StatusBarViewModel
from .viewmodels.tile import TileViewModel, VirtualTileViewModel
from .viewmodels.tileset import TilesetViewModel
from .viewmodels.winner import WinnerViewModel


class GameViewModel:
    """The viewmodel of the game view."""

    __slots__ = (
        "_board",
        "_board_service",
        "_players",
        "_rack",
        "_pile",
        "_winner",
        "_status_bar",
        "_user_id",
        "_events_observer",
        "_store",
        "_scroll_service",
        "__weakref__",
    )

    @property
    def board(self) -> tuple[tuple[TilesetViewModel, ...], ...]:
        """Rows of the game board."""
        return self._board

    @property
    def players(self) -> tuple[PlayerViewModel, ...]:
        """Players currently participating in the game."""
        return self._players

    @property
    def rack(self) -> TilesetViewModel:
        """The user's rack."""
        return self._rack

    @property
    def pile(self) -> PileViewModel:
        """The current pile of tiles to draw from."""
        return self._pile

    @property
    def winner(self) -> WinnerViewModel | None:
        """The optional winner of the game."""
        return self._winner

    @property
    def status_bar(self) -> StatusBarViewModel:
        """The status bar showing the selection mode and a turn status."""
        return self._status_bar

    def __init__(
        self,
        board_service: BoardService,
        events_observer: EventsObserver,
        scroll_service: ScrollService,
        store: Store[GameScreenState],
        user_id: str,
    ):
        self._board_service: BoardService = board_service
        self._events_observer: EventsObserver = events_observer
        self._scroll_service: ScrollService = scroll_service
        self._store: Store[GameScreenState] = store

        self._board: tuple[tuple[TilesetViewModel, ...], ...] = ()
        self._rack: TilesetViewModel = TilesetViewModel(tiles=(), is_highlighted=False)
        self._players: tuple[PlayerViewModel, ...] = ()
        self._pile: PileViewModel = PileViewModel(pile_count=0)
        self._winner: WinnerViewModel | None = None
        self._status_bar: StatusBarViewModel = StatusBarViewModel(
            selection_mode=SelectionMode.TILES, has_turn=False
        )
        self._user_id: str = user_id

    def on_state(self, state: GameScreenState) -> None:
        """The hook of the store subscriber.

        Creates viewmodels for all game widgets according to the new state, and
        signals for app redraw.
        """
        highlighted_tile: Tile | None = (
            state.highlighted_tile
            if state.selection_mode == SelectionMode.TILES
            else None
        )
        self._board = self._create_board_and_update_scroll_maps(state=state)
        self._rack = TilesetViewModel(
            tiles=tuple(
                TileViewModel(
                    tile=tile,
                    is_selected=tile in state.selected_tiles,
                    is_highlighted=tile == highlighted_tile,
                    is_new=tile in state.new_tiles,
                )
                for tile in state.rack.tiles
            ),
            is_highlighted=False,
        )
        self._players = tuple(PlayerViewModel(player=player) for player in state.players)
        self._pile = PileViewModel(pile_count=state.pile_count)
        self._winner = None if not state.winner else WinnerViewModel(winner=state.winner)
        self._status_bar = StatusBarViewModel(
            selection_mode=state.selection_mode,
            has_turn=next(
                (p.has_turn for p in state.players if p.user_id == self._user_id), False
            ),
        )

        application.get_app().invalidate()

    def subscribe(self) -> None:
        self._store.subscribe(self, include_current=True)
        self._events_observer.observe()

    def unsubscribe(self) -> None:
        self._store.unsubscribe(self)
        self._events_observer.stop()

    def _create_board_and_update_scroll_maps(
        self, state: GameScreenState
    ) -> tuple[tuple[TilesetViewModel, ...], ...]:
        highlighted_tile: Tile | None = (
            state.highlighted_tile
            if state.selection_mode == SelectionMode.TILES
            else None
        )
        highlighted_tileset: Tileset | None = (
            state.highlighted_tileset
            if state.selection_mode == SelectionMode.TILESETS
            else None
        )
        selected_tiles: frozenset[Tile] = state.selected_tiles
        new_tiles: frozenset[Tile] = state.new_tiles
        rows = self._board_service.create_rows(board=state.board.tilesets)
        board = tuple(
            tuple(
                TilesetViewModel(
                    tiles=tuple(
                        TileViewModel(
                            tile=tile,
                            is_selected=tile in selected_tiles,
                            is_highlighted=tile == highlighted_tile,
                            is_new=tile in new_tiles,
                        )
                        for tile in tileset.tiles
                    ),
                    is_highlighted=tileset == highlighted_tileset,
                )
                for tileset in row
            )
            for row in rows
        )

        if state.selection_mode == SelectionMode.TILESETS:
            board = (
                *board,
                (
                    TilesetViewModel(
                        tiles=tuple(
                            VirtualTileViewModel(
                                tile=tile,
                                is_selected=tile in selected_tiles,
                                is_highlighted=tile == highlighted_tile,
                                is_new=tile in new_tiles,
                            )
                            for tile in state.virtual_tileset.tiles
                        ),
                        is_highlighted=state.virtual_tileset == highlighted_tileset
                        and isinstance(highlighted_tileset, VirtualTileset),
                    ),
                ),
            )

        self._scroll_service.update_scroll_maps(
            board=rows, virtual_tileset=state.virtual_tileset, rack=state.rack
        )

        return board
