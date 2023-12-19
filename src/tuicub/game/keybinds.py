from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from pydepot import Store

from ..common.keybinds.container import KeybindsContainer
from ..common.models import Keybind, Player
from ..common.state import State
from ..common.strings import (
    ARROW_LEFT,
    ARROW_RIGHT,
    ARROW_UP,
    ARROWS_ALL,
    GAME_DRAW_KEY_TOOLTIP,
    GAME_END_TURN_KEY_TOOLTIP,
    GAME_FINISH_GAME_KEY_TOOLTIP,
    GAME_MOVE_MODE_KEY_TOOLTIP,
    GAME_MOVE_TILES_KEY_TOOLTIP,
    GAME_REDO_KEY_TOOLTIP,
    GAME_SELECT_MODE_KEY_TOOLTIP,
    GAME_TOGGLE_SELECTED_KEY_TOOLTIP,
    GAME_UNDO_KEY_TOOLTIP,
)
from .controller import GameController
from .models import ScrollDirection, SelectionMode
from .state import GameScreenState


class GameKeybindsContainer(KeybindsContainer):
    """The container for keybinds of the game screen."""

    __slots__ = ("_controller", "_store", "_local_store")

    def __init__(
        self,
        controller: GameController,
        store: Store[State],
        local_store: Store[GameScreenState],
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize new container.

        Args:
            controller (GameController): The controller for capturing key presses.
            store (Store[State]): The global store.
            local_store (Store[GameScreenState]): The local screen store.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        self._controller: GameController = controller
        self._store: Store[State] = store
        self._local_store: Store[GameScreenState] = local_store
        super().__init__(*args, **kwargs)

    def keybinds(self) -> Sequence[Keybind]:
        """Returns keybinds for the game screen.

        Gamerooms screen has following keybinds:
            * "h": scrolls the game board to the left,
            * "j": scrolls the game board down,
            * "k": scrolls the game board up,
            * "l": scrolls the game board to the right,
            * "u": performs an undo game action,
            * "r": performs a redo game action,
            * "e": performs an end turn game action,
            * "d": performs a draw game action,
            * "s": sets the select tiles mode,
            * "m": sets the move tiles mode,
            * "space": toggles the select state of the currently highlighted tile,
            * "enter": performs the move tiles game action if the game is running,
                or finished the game if the game has ended.

        Returns:
            The list of keybinds.
        """
        has_turn_no_winner = HasTurnNoWinner(
            store=self._store, local_store=self._local_store
        )
        has_winner = HasWinner(store=self._store, local_store=self._local_store)
        has_turn_no_winner_tiles_selection = HasTurnNoWinnerTilesSelectionMode(
            store=self._store, local_store=self._local_store
        )
        has_turn_no_winner_tilesets_selection = HasTurnNoWinnerTilesetsSelectionMode(
            store=self._store, local_store=self._local_store
        )

        return [
            Keybind(
                key=("h", "left"),
                display_key="h",
                tooltip=ARROW_LEFT,
                action=lambda _: self._controller.scroll(ScrollDirection.LEFT),
                condition=has_turn_no_winner,
                is_hidden=True,
            ),
            Keybind(
                key=("j", "down"),
                display_key="hjkl",
                tooltip=ARROWS_ALL,
                action=lambda _: self._controller.scroll(ScrollDirection.DOWN),
                condition=has_turn_no_winner,
                is_hidden=False,
            ),
            Keybind(
                key="k",
                display_key="k",
                tooltip=ARROW_UP,
                action=lambda _: self._controller.scroll(ScrollDirection.UP),
                condition=has_turn_no_winner,
                is_hidden=True,
            ),
            Keybind(
                key=("l", "right"),
                display_key="k",
                tooltip=ARROW_RIGHT,
                action=lambda _: self._controller.scroll(ScrollDirection.RIGHT),
                condition=has_turn_no_winner,
                is_hidden=True,
            ),
            Keybind(
                key="u",
                display_key="u",
                tooltip=GAME_UNDO_KEY_TOOLTIP,
                action=self._controller.undo,
                condition=has_turn_no_winner,
            ),
            Keybind(
                key="r",
                display_key="r",
                tooltip=GAME_REDO_KEY_TOOLTIP,
                action=self._controller.redo,
                condition=has_turn_no_winner,
            ),
            Keybind(
                key="e",
                display_key="e",
                tooltip=GAME_END_TURN_KEY_TOOLTIP,
                action=self._controller.end_turn,
                condition=has_turn_no_winner,
            ),
            Keybind(
                key="d",
                display_key="d",
                tooltip=GAME_DRAW_KEY_TOOLTIP,
                action=self._controller.draw,
                condition=has_turn_no_winner,
            ),
            Keybind(
                key="s",
                display_key="s",
                tooltip=GAME_SELECT_MODE_KEY_TOOLTIP,
                action=self._controller.set_tiles_selection,
                condition=has_turn_no_winner_tilesets_selection,
            ),
            Keybind(
                key="m",
                display_key="m",
                tooltip=GAME_MOVE_MODE_KEY_TOOLTIP,
                action=self._controller.set_tilesets_selection,
                condition=has_turn_no_winner_tiles_selection,
            ),
            Keybind(
                key="space",
                display_key="space",
                tooltip=GAME_TOGGLE_SELECTED_KEY_TOOLTIP,
                action=self._controller.toggle_tile_selected,
                condition=has_turn_no_winner_tiles_selection,
            ),
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=GAME_MOVE_TILES_KEY_TOOLTIP,
                action=self._controller.move_tiles,
                condition=has_turn_no_winner_tilesets_selection,
            ),
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=GAME_FINISH_GAME_KEY_TOOLTIP,
                action=self._controller.finish_game,
                condition=has_winner,
            ),
        ]


class Condition(ABC):
    """Base class for game keybind condition."""

    __slots__ = ("_store", "_local_store")

    def __init__(self, store: Store[State], local_store: Store[GameScreenState]):
        """Initialize new condition.

        Args:
            store (Store[State]): The global store.
            local_store (Store[GameScreenState]): The local screen store.
        """
        self._store: Store[State] = store
        self._local_store: Store[GameScreenState] = local_store

    @abstractmethod
    def __call__(self) -> bool:
        """Returns true if keybind should be active, false otherwise."""


class HasTurnNoWinner(Condition):
    __slots__ = ()

    def __call__(self) -> bool:
        has_winner = self._local_store.state.winner is not None

        return (
            _has_turn(local_store=self._local_store, store=self._store) and not has_winner
        )


class HasWinner(Condition):
    __slots__ = ()

    def __call__(self) -> bool:
        return self._local_store.state.winner is not None


class HasTurnNoWinnerTilesSelectionMode(HasTurnNoWinner):
    __slots__ = ()

    def __call__(self) -> bool:
        return (
            super().__call__()
            and self._local_store.state.selection_mode == SelectionMode.TILES
        )


class HasTurnNoWinnerTilesetsSelectionMode(HasTurnNoWinner):
    __slots__ = ()

    def __call__(self) -> bool:
        return (
            super().__call__()
            and self._local_store.state.selection_mode == SelectionMode.TILESETS
        )


def _has_turn(local_store: Store[GameScreenState], store: Store[State]) -> bool:
    user_id = store.state.current_user.id if store.state.current_user else ""
    players = local_store.state.players
    player: Player | None = next(
        (player for player in players if player.user_id == user_id), None
    )

    return player.has_turn if player else False
