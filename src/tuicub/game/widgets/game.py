from prompt_toolkit.layout.screen import Screen

from ...common.views import Color, Theme
from ..viewmodels.pile import PileViewModel
from ..viewmodels.player import PlayerViewModel
from ..viewmodels.status_bar import StatusBarViewModel
from ..viewmodels.tileset import TilesetViewModel
from ..viewmodels.winner import WinnerViewModel
from .base import BaseWidget, Frame
from .board import BoardWidget
from .rack import RackWidget
from .renderer import Position, Renderer, Side
from .status_bar import StatusBarWidget
from .top_bar import TopBarWidget
from .winner import WinnerWidget


class GameWidget(BaseWidget):
    """The widget containing all game widgets."""

    __slots__ = ("_theme", "_rack", "_board", "_status_bar", "_top_bar", "_winner")

    def __init__(
        self,
        board: tuple[tuple[TilesetViewModel, ...], ...],
        rack: TilesetViewModel,
        pile: PileViewModel,
        players: tuple[PlayerViewModel, ...],
        status_bar: StatusBarViewModel,
        winner: WinnerViewModel | None,
        theme: Theme | None = None,
    ) -> None:
        self._theme: Theme = theme or Theme.default()
        self._rack = RackWidget(viewmodel=rack, theme=self._theme)
        self._board = BoardWidget(board=board, theme=self._theme)
        self._status_bar = StatusBarWidget(viewmodel=status_bar, theme=self._theme)
        self._top_bar = TopBarWidget(pile=pile, players=players, theme=self._theme)
        self._winner: WinnerWidget | None = (
            None if not winner else WinnerWidget(viewmodel=winner, theme=self._theme)
        )

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        if winner := self._winner:
            renderer.render_widget(
                widget=winner,
                position=Position.CENTER,
                side=Side.CENTER,
                screen=screen,
                frame=frame,
                width=winner.width,
            )
        else:
            renderer.render_widget(
                widget=self._status_bar,
                position=Position.BOTTOM,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
            )
            renderer.render_widget(
                widget=self._rack,
                position=Position.BOTTOM,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
                y_offset=self._status_bar.height,
            )
            renderer.render_widget(
                widget=self._board,
                position=Position.TOP,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
                height=frame.height - (self._top_bar.height + self._rack.height),
                y_offset=self._top_bar.height,
            )

        renderer.render_widget(
            widget=self._top_bar,
            position=Position.TOP,
            side=Side.LEFT,
            screen=screen,
            frame=frame,
            width=frame.width,
        )

        renderer.set_background_color(Color.BG2, screen, frame)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameWidget):
            return NotImplemented

        return (
            self._rack == other._rack
            and self._board == other._board
            and self._status_bar == other._status_bar
            and self._top_bar == other._top_bar
            and self._winner == other._winner
        )
