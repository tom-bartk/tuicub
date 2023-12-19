from abc import abstractmethod
from typing import Protocol

from prompt_toolkit import application
from prompt_toolkit.key_binding import KeyBindings, KeyBindingsBase
from prompt_toolkit.layout import AnyContainer
from prompt_toolkit.layout.layout import FocusableElement

from ...common.keybinds.container import KeybindsContainer


class KeybindableElement(Protocol):
    """A view that is capable of attaching key bindings."""

    @property
    @abstractmethod
    def key_bindings(self) -> KeyBindingsBase | None:
        """The attached key bindings."""

    @key_bindings.setter
    @abstractmethod
    def key_bindings(self, value: KeyBindingsBase | None) -> None:
        """Attach new key bindings."""


class RootScreenView:
    """A root view of a screen."""

    __slots__ = ("_key_bindings", "_keybinds_container", "__weakref__")

    def __init__(
        self,
        keybinds_container: KeybindsContainer,
        key_bindings: KeyBindings | None = None,
    ):
        """Initialize new view.

        Args:
            keybinds_container (KeybindsContainer): The container for keybinds
                of the screen.
            key_bindings (KeyBindings | None): The optional `prompt_toolkit` key bindings.
        """
        self._key_bindings: KeyBindings = key_bindings or KeyBindings()
        self._keybinds_container: KeybindsContainer = keybinds_container
        self._attach_keybinds()

    def did_appear(self) -> None:
        """A hook called whenever the screen appears."""
        application.get_app().layout.focus(self.focus_target())

    def will_appear(self) -> None:
        """A hook called before the screen will appear."""

    def will_disappear(self) -> None:
        """A hook called before the screen will disappear."""

    @abstractmethod
    def focus_target(self) -> FocusableElement:
        """The view to focus whenever the screen appears."""

    @abstractmethod
    def keybinds_target(self) -> KeybindableElement:
        """The view to attach the keybinds to."""

    @abstractmethod
    def __pt_container__(self) -> AnyContainer:
        """The `prompt_toolkit.container.AnyContainer` protocol signature."""

    def _attach_keybinds(self) -> None:
        self._keybinds_container.attach(self._key_bindings)
        target = self.keybinds_target()
        target.key_bindings = self._key_bindings
