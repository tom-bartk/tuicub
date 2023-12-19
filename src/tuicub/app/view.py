from prompt_toolkit.application import get_app
from prompt_toolkit.layout import DynamicContainer, HSplit
from pyllot import ScreenPresenting

from ..common.screens import TuicubScreen
from ..common.views import Color, TextView, Theme
from .status import StatusView
from .viewmodel import AppViewModel


class AppView(HSplit, ScreenPresenting[TuicubScreen]):
    """A root view of the application that presents screens."""

    def __init__(
        self,
        viewmodel: AppViewModel,
        status_view: StatusView,
        initial_screen: TuicubScreen,
        theme: Theme,
    ) -> None:
        self._viewmodel: AppViewModel = viewmodel
        self._screen: TuicubScreen = initial_screen
        self._container: DynamicContainer = DynamicContainer(self.screen)
        super().__init__(
            [
                self._container,
                status_view,
                TextView(self._viewmodel.keybinds, theme=theme),
            ],
            style=theme.to_framework_bg(color=Color.BG1),
        )
        self._viewmodel.bind_keybinds(initial_screen.keybinds)
        self._viewmodel.subscribe()

    def present(self, screen: TuicubScreen) -> None:
        self._screen = screen
        self._viewmodel.bind_keybinds(screen.keybinds)
        get_app().invalidate()

    def screen(self) -> TuicubScreen:
        return self._screen
