from abc import abstractmethod
from collections.abc import Sequence
from typing import Generic, Protocol, TypeVar
from weakref import ReferenceType, ref

from prompt_toolkit.layout import AnyContainer
from pyllot import ScreenBase

from ..keybinds.container import KeybindsContainer
from ..models import Keybind
from .root_view import RootScreenView


class ScreenLifecycleDelegate(Protocol):
    """Delegate receiving callbacks of the screen lifecycle."""

    @abstractmethod
    def screen_did_present(self, screen: "TuicubScreen") -> None:
        """Called whenever the screen appears.

        Args:
            screen (TuicubScreen): The screen that appeared.
        """


TView = TypeVar("TView", bound=RootScreenView, covariant=True)


class TuicubScreen(Generic[TView], ScreenBase):
    """Base class for application screens."""

    __slots__ = ("_delegate", "_keybinds_container", "_view", "__weakref__")

    def __init__(self, view: TView, keybinds_container: KeybindsContainer):
        """Initialize new screen.

        Args:
            view (TView): The root view of the screen.
            keybinds_container (KeybindsContainer): The container for keybinds
                of the screen.
        """
        self._delegate: ReferenceType[ScreenLifecycleDelegate] | None = None
        self._keybinds_container: KeybindsContainer = keybinds_container
        self._view: TView = view

    def did_present(self) -> None:
        if self._delegate and (delegate := self._delegate()):
            delegate.screen_did_present(self)
        self._view.did_appear()

    def will_present(self) -> None:
        self._view.will_appear()

    def will_disappear(self) -> None:
        self._view.will_disappear()

    def keybinds(self) -> Sequence[Keybind]:
        """Returns keybinds to display in the keybinds widget."""
        return self._keybinds_container.keybinds()

    def set_delegate(self, delegate: ScreenLifecycleDelegate) -> None:
        self._delegate = ref(delegate)

    def __pt_container__(self) -> AnyContainer:
        return self._view
