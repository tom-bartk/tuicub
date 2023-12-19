from collections.abc import Sequence
from typing import Any

from ..common.keybinds.container import KeybindsContainer
from ..common.models import Keybind
from ..common.strings import (
    ARROW_DOWN,
    ARROW_UP,
    GAMEROOMS_CREATE_GAMEROOM_KEY_TOOLTIP,
    GAMEROOMS_JOIN_GAMEROOM_KEY_TOOLTIP,
    GAMEROOMS_REFRESH_KEY_TOOLTIP,
)
from .controller import GameroomsController


class GameroomsKeybindsContainer(KeybindsContainer):
    """The container for keybinds of the gamerooms screen."""

    __slots__ = ("_controller",)

    def __init__(self, controller: GameroomsController, *args: Any, **kwargs: Any):
        """Initialize new container.

        Args:
            controller (GameroomsController): The controller for capturing key presses.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        self._controller: GameroomsController = controller
        super().__init__(*args, **kwargs)

    def keybinds(self) -> Sequence[Keybind]:
        """Returns keybinds for the gamerooms screen.

        The gamerooms screen has following keybinds:
            * "j": scrolls the gamerooms list down,
            * "k": scrolls the gamerooms list up,
            * "c": sends a create gameroom request,
            * "r": sends a get gamerooms request,
            * "enter": sends the join gameroom request.

        Returns:
            The list of keybinds.
        """
        return [
            Keybind(
                key="j",
                display_key="j",
                tooltip=ARROW_DOWN,
                action=self._controller.scroll_gamerooms_down,
            ),
            Keybind(
                key="k",
                display_key="k",
                tooltip=ARROW_UP,
                action=self._controller.scroll_gamerooms_up,
            ),
            Keybind(
                key="c",
                display_key="c",
                tooltip=GAMEROOMS_CREATE_GAMEROOM_KEY_TOOLTIP,
                action=self._controller.create_gameroom,
            ),
            Keybind(
                key="r",
                display_key="r",
                tooltip=GAMEROOMS_REFRESH_KEY_TOOLTIP,
                action=self._controller.refresh_gamerooms,
            ),
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=GAMEROOMS_JOIN_GAMEROOM_KEY_TOOLTIP,
                action=self._controller.join_gameroom,
            ),
        ]
