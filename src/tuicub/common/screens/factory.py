from collections.abc import Callable

from pyllot import ScreensFactoryBase

from .tuicub_screen import TuicubScreen


class ScreensFactory(ScreensFactoryBase[TuicubScreen]):
    """A factory for creating application screens."""

    __slots__ = ("_factories",)

    def __init__(self) -> None:
        self._factories: dict[str, Callable[[], TuicubScreen]] = {}

    def create(self, screen_name: str) -> TuicubScreen:
        """Create a new screen based on its name.

        Args:
            screen_name (str): The name of the screen to create.

        Returns:
            The created screen.
        """
        if factory := self._factories.get(screen_name, None):
            return factory()
        raise NotImplementedError

    def add_factory(self, name: str, factory: Callable[[], TuicubScreen]) -> None:
        """Registers a factory that creates a screen for the given name.

        Args:
            name (str): The name of the screen that the factory creates.
            factory (Callable[[], TuicubScreen]): The factory of the screen.
        """
        self._factories[name] = factory
