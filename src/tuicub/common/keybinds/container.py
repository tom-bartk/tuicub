from abc import ABC, abstractmethod
from collections.abc import Sequence

from prompt_toolkit.key_binding.key_bindings import KeyBindings
from pydepot import Store

from ...app.state import AppState
from ..models import Keybind
from ..utils import create_filter


class KeybindsContainer(ABC):
    """Base class for a keybinds container."""

    __slots__ = ("_app_store",)

    def __init__(self, app_store: Store[AppState]):
        """Initialize new container.

        Args:
            app_store (Store[AppState]): The store of the app state.
        """
        self._app_store: Store[AppState] = app_store

    @abstractmethod
    def keybinds(self) -> Sequence[Keybind]:
        """Returns a list of keybinds for this container."""

    def attach(self, bindings: KeyBindings) -> None:
        """Attach keybinds to the `prompt_toolkit` bindings.

        Args:
            bindings (KeyBindings): The `prompt_toolkit` bindings.
        """
        for keybind in self.keybinds():
            _filter = create_filter(app_store=self._app_store, keybind=keybind)
            if isinstance(keybind.key, tuple):
                for kb in keybind.key:
                    bindings.add(kb, filter=_filter)(keybind.action)
            else:
                bindings.add(keybind.key, filter=_filter)(keybind.action)
