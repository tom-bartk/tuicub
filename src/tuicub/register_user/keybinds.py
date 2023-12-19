from collections.abc import Sequence
from typing import Any

from prompt_toolkit.filters import Always

from ..common.keybinds.container import KeybindsContainer
from ..common.models import Keybind
from ..common.strings import REGISTER_USER_SUBMIT_KEY_TOOLTIP
from .controller import RegisterUserController


class RegisterUserKeybindsContainer(KeybindsContainer):
    """The container for keybinds of the register user screen."""

    __slots__ = ("_controller",)

    def __init__(self, controller: RegisterUserController, *args: Any, **kwargs: Any):
        """Initialize new container.

        Args:
            controller (RegisterUserController): The controller for capturing key presses.
            *args (Any): Additional positional arguments.
            **kwargs (Any): Additional keyword arguments.
        """
        self._controller: RegisterUserController = controller
        super().__init__(*args, **kwargs)

    def keybinds(self) -> Sequence[Keybind]:
        """The register user screen keybinds.

        Register user screen has following keybinds:
            * "enter": sends the register user requests.

        Returns:
            The list of keybinds.
        """
        return [
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=REGISTER_USER_SUBMIT_KEY_TOOLTIP,
                action=self._controller.register_user,
                pt_filter=Always(),
            )
        ]
