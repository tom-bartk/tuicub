from prompt_toolkit.key_binding import KeyPressEvent
from pydepot import Store

from ..common import utils
from ..common.state import State
from .requests import (
    DeleteGameroomInteractor,
    LeaveGameroomInteractor,
    StartGameInteractor,
)


class GameroomController:
    """Captures and converts user input to interactions in the gameroom screen."""

    def __init__(
        self,
        store: Store[State],
        delete_gameroom_interactor: DeleteGameroomInteractor,
        leave_gameroom_interactor: LeaveGameroomInteractor,
        start_game_interactor: StartGameInteractor,
    ):
        """Initialize new controller.

        Args:
            store (Store[State]): The global store.
            delete_gameroom_interactor (DeleteGameroomInteractor): The interactor for
                the delete gameroom request.
            leave_gameroom_interactor (LeaveGameroomInteractor): The interactor for
                the leave gameroom request.
            start_game_interactor (StartGameInteractor): The interactor for
                the start game request.
        """
        self._store: Store[State] = store
        self._delete_gameroom_interactor: DeleteGameroomInteractor = (
            delete_gameroom_interactor
        )
        self._leave_gameroom_interactor: LeaveGameroomInteractor = (
            leave_gameroom_interactor
        )
        self._start_game_interactor: StartGameInteractor = start_game_interactor

    def delete_gameroom(self, event: KeyPressEvent) -> None:
        """Handler for the delete gameroom keybind.

        Sends a delete gameroom request.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        utils.async_run(self._delete_gameroom_interactor.execute())

    def leave_gameroom(self, event: KeyPressEvent) -> None:
        """Handler for the leave gameroom keybind.

        Sends a leave gameroom request.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        utils.async_run(self._leave_gameroom_interactor.execute())

    def start_game(self, event: KeyPressEvent) -> None:
        """Handler for the start game keybind.

        Sends a start game request.

        Args:
            event (KeyPressEvent): The triggering event.
        """
        utils.async_run(self._start_game_interactor.execute())
