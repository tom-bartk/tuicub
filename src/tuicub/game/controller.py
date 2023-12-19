from prompt_toolkit.key_binding import KeyPressEvent
from pydepot import Store

from ..common.models import Alert, AlertType
from ..common.services.alert_service import AlertService
from ..common.state import FinishGameAction, State
from ..common.strings import GAME_NO_TILES_SELECTED_ALERT
from .actions import (
    SetTilesetsSelectionAction,
    SetTilesSelectionAction,
    ToggleTileSelectedAction,
)
from .interactors.actions import ActionsInteractor
from .interactors.scroll import ScrollInteractor
from .models import ScrollDirection
from .state import GameScreenState


class GameController:
    """Captures and converts user input to interactions in the game screen."""

    __slots__ = (
        "_actions_interactor",
        "_alert_service",
        "_local_store",
        "_scroll_interactor",
        "_store",
    )

    def __init__(
        self,
        actions_interactor: ActionsInteractor,
        alert_service: AlertService,
        local_store: Store[GameScreenState],
        scroll_interactor: ScrollInteractor,
        store: Store[State],
    ):
        """Initialize new controller.

        Args:
            actions_interactor (ActionsInteractor): The interactor for game actions.
            alert_service (AlertService): The alert service.
            local_store (Store[GameScreenState]): The local screen store.
            scroll_interactor (ScrollInteractor): The game scrolling interactor.
            store (Store[State]): The global store.
        """
        self._actions_interactor: ActionsInteractor = actions_interactor
        self._alert_service: AlertService = alert_service
        self._local_store: Store[GameScreenState] = local_store
        self._scroll_interactor: ScrollInteractor = scroll_interactor
        self._store: Store[State] = store

    def scroll(self, direction: ScrollDirection) -> None:
        """Handler for the scroll game board keybind.

        Scrolls the game board in the given direction.

        Args:
            direction (ScrollDirection): The direction to scroll to.
        """
        self._scroll_interactor.scroll(direction=direction)

    def toggle_tile_selected(self, event: KeyPressEvent) -> None:
        """Handler for the toggle tile selected keybind.

        Dispatches a `ToggleTileSelectedAction` to the local store.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._local_store.dispatch(ToggleTileSelectedAction())

    def set_tiles_selection(self, event: KeyPressEvent) -> None:
        """Handler for the set select mode keybind.

        Dispatches a `SetTilesSelectionAction` to the local store.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._local_store.dispatch(SetTilesSelectionAction())

    def set_tilesets_selection(self, event: KeyPressEvent) -> None:
        """Handler for the set move mode keybind.

        Dispatches a `SetTilesetsSelectionAction` to the local store if the user
        has at least one selected tile. If no tiles are selected, queues a warning alert.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        if not self._local_store.state.selected_tiles:
            self._alert_service.queue_alert(
                Alert(GAME_NO_TILES_SELECTED_ALERT, AlertType.WARNING)
            )
            return
        self._local_store.dispatch(SetTilesetsSelectionAction())

    def move_tiles(self, event: KeyPressEvent) -> None:
        """Handler for the move tiles keybind.

        Performs a move tiles game action.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._actions_interactor.move_tiles()

    def undo(self, event: KeyPressEvent) -> None:
        """Handler for the undo keybind.

        Performs an undo game action.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._actions_interactor.undo()

    def redo(self, event: KeyPressEvent) -> None:
        """Handler for the redo keybind.

        Performs a redo game action.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._actions_interactor.redo()

    def end_turn(self, event: KeyPressEvent) -> None:
        """Handler for the end turn keybind.

        Performs an end turn game action.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._actions_interactor.end_turn()

    def draw(self, event: KeyPressEvent) -> None:
        """Handler for the draw keybind.

        Performs a draw game action.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._actions_interactor.draw()

    def finish_game(self, event: KeyPressEvent) -> None:
        """Handler for the finish game keybind.

        Dispatches a `FinishGameAction` to the global store.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        self._store.dispatch(FinishGameAction())
