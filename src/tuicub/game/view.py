from __future__ import annotations

from typing import Any

from prompt_toolkit.key_binding import KeyBindingsBase
from prompt_toolkit.layout import AnyContainer, Container
from prompt_toolkit.layout.layout import FocusableElement
from prompt_toolkit.layout.mouse_handlers import MouseHandlers
from prompt_toolkit.layout.screen import Screen, WritePosition

from ..common.screens import KeybindableElement, RootScreenView, ScreenName, TuicubScreen
from ..common.views import FocusWindow, Theme
from ..common.views.base_container import BasicContainer
from .viewmodel import GameViewModel
from .widgets.frame import Frame
from .widgets.game import GameWidget
from .widgets.renderer import Renderer


class GameWidgetFactory:
    """A factory creating instances of the game widget."""

    __slots__ = ("_viewmodel", "_theme")

    def __init__(self, viewmodel: GameViewModel, theme: Theme | None = None):
        """Initialize new factory.

        Args:
            viewmodel (GameViewModel): The viewmodel of the game view.
            theme (Theme | None): An optional theme.
        """
        self._viewmodel: GameViewModel = viewmodel
        self._theme: Theme = theme or Theme.default()

    def create(self) -> GameWidget:
        """Creates a new instance of the game widget."""
        return GameWidget(
            board=self._viewmodel.board,
            rack=self._viewmodel.rack,
            pile=self._viewmodel.pile,
            players=self._viewmodel.players,
            status_bar=self._viewmodel.status_bar,
            winner=self._viewmodel.winner,
            theme=self._theme,
        )


class GameView(RootScreenView):
    """The root view of the game screen."""

    __slots__ = ("_viewmodel", "_game_root_view")

    def __init__(
        self,
        viewmodel: GameViewModel,
        game_root_view: GameRootView,
        *args: Any,
        **kwargs: Any,
    ):
        self._game_root_view = game_root_view
        self._viewmodel: GameViewModel = viewmodel

        super().__init__(*args, **kwargs)

    def did_appear(self) -> None:
        super().did_appear()
        self._viewmodel.subscribe()

    def will_disappear(self) -> None:
        super().will_disappear()
        self._viewmodel.unsubscribe()

    def focus_target(self) -> FocusableElement:
        return self._game_root_view.focus_target()

    def keybinds_target(self) -> KeybindableElement:
        return self._game_root_view

    def __pt_container__(self) -> AnyContainer:
        return self._game_root_view


class GameRootView(BasicContainer):
    """A container for the game widget.."""

    __slots__ = ("_factory", "_renderer", "_focus_window")

    @property
    def key_bindings(self) -> KeyBindingsBase | None:
        return self._focus_window.control.key_bindings

    @key_bindings.setter
    def key_bindings(self, value: KeyBindingsBase | None) -> None:
        self._focus_window.control.key_bindings = value

    def __init__(
        self, factory: GameWidgetFactory, focus_window: FocusWindow, renderer: Renderer
    ):
        self._factory: GameWidgetFactory = factory
        self._renderer: Renderer = renderer
        self._focus_window: FocusWindow = focus_window

    def get_children(self) -> list[Container]:
        return [self._focus_window]

    def write_to_screen(
        self,
        screen: Screen,
        mouse_handlers: MouseHandlers,
        write_position: WritePosition,
        parent_style: str,
        erase_bg: bool,
        z_index: int | None,
    ) -> None:
        game_widget = self._factory.create()
        game_widget.render(
            renderer=self._renderer,
            screen=screen,
            frame=Frame.from_write_position(write_position),
        )
        screen.height = max(screen.height, write_position.height)

    def get_key_bindings(self) -> KeyBindingsBase | None:
        return self._focus_window.control.get_key_bindings()

    def focus_target(self) -> FocusableElement:
        return self._focus_window


class GameScreen(TuicubScreen[GameView]):
    @property
    def screen_name(self) -> str:
        return ScreenName.GAME
