from typing import Generic, TypeVar

from pydepot import Action, Store

from ..logger import Logger

_TState = TypeVar("_TState")


class TuicubStore(Generic[_TState], Store[_TState]):
    """A state store that logs dispatched actions."""

    __slots__ = ("_logger",)

    def __init__(self, initial_state: _TState, logger: Logger):
        self._logger: Logger = logger
        super().__init__(initial_state=initial_state)

    def dispatch(self, action: Action) -> None:
        self._logger.log_action(action=action)
        super().dispatch(action=action)
