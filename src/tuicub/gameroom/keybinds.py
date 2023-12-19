from collections.abc import Callable, Sequence
from typing import Any

from pydepot import Store

from ..common.keybinds.container import KeybindsContainer
from ..common.models import Keybind
from ..common.state import State
from ..common.strings import (
    GAMEROOM_DELETE_GAMEROOM_KEY_TOOLTIP,
    GAMEROOM_LEAVE_GAMEROOM_KEY_TOOLTIP,
    GAMEROOM_START_GAME_KEY_TOOLTIP,
)
from .controller import GameroomController


class GameroomKeybindsContainer(KeybindsContainer):
    """The container for keybinds of the gameroom screen."""

    __slots__ = ("_controller", "_store")

    def __init__(
        self,
        controller: GameroomController,
        store: Store[State],
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize new container.

        Args:
            controller (GameroomController): The controller for capturing key presses.
            store (Store[State]): The global store.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        self._controller: GameroomController = controller
        self._store: Store[State] = store
        super().__init__(*args, **kwargs)

    def keybinds(self) -> Sequence[Keybind]:
        """Returns keybinds for the gameroom screen.

        The gameroom screen has following keybinds:
            * "d": sends a delete gameroom request if user is the owner,
            * "l": sends a leave gameroom request if user is not the owner,
            * "s": sends a start game request if user is the owner,

        Returns:
            The list of keybinds.
        """
        is_owner = _is_owner_condition(self._store)

        return [
            Keybind(
                key="d",
                display_key="d",
                tooltip=GAMEROOM_DELETE_GAMEROOM_KEY_TOOLTIP,
                action=self._controller.delete_gameroom,
                condition=is_owner,
            ),
            Keybind(
                key="l",
                display_key="l",
                tooltip=GAMEROOM_LEAVE_GAMEROOM_KEY_TOOLTIP,
                action=self._controller.leave_gameroom,
                condition=lambda: not is_owner(),
            ),
            Keybind(
                key="s",
                display_key="s",
                tooltip=GAMEROOM_START_GAME_KEY_TOOLTIP,
                action=self._controller.start_game,
                condition=is_owner,
            ),
        ]


def _is_owner_condition(store: Store[State]) -> Callable[[], bool]:
    """Returns a filter returning true, if the user owns the current gameroom."""

    def wrapped() -> bool:
        state: State = store.state
        owner_id = state.current_gameroom.owner_id if state.current_gameroom else None
        user_id = state.current_user.id if state.current_user else None

        return user_id is not None and owner_id is not None and owner_id == user_id

    return wrapped
