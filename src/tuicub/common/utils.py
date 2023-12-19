import asyncio
from collections.abc import Coroutine
from typing import TypeVar

from prompt_toolkit.filters import Condition, Filter
from pydepot import Store

from ..app.state import AppState
from .models import Keybind

_T = TypeVar("_T")


def async_run(coro: Coroutine[_T, None, None]) -> None:
    """Runs the coroutine in the currently running loop."""
    task = asyncio.get_running_loop().create_task(coro)
    tasks: set[asyncio.Task] = {task}
    task.add_done_callback(tasks.discard)


def create_filter(app_store: Store[AppState], keybind: Keybind) -> Filter:
    """Create a filter for the keybind.

    Args:
        app_store (Store[AppState]): The store for the app state.
        keybind (Keybind[_T]): The keybind to create the filter for.

    Returns:
        The created filter.
    """

    def wrapped() -> bool:
        return (
            app_store.state.confirmation is None
            and keybind.pt_filter()
            and keybind.condition()
        )

    return Condition(wrapped)
