from prompt_toolkit.layout.screen import Screen

from ...common.views import Color, Theme
from ..viewmodels.pile import PileViewModel
from ..viewmodels.player import PlayerViewModel
from .base import BaseWidget, Frame
from .pile import PileWidget
from .players_list import PlayersListWidget
from .renderer import Position, Renderer, SeparatorSide, Side

HEIGHT = 3
PADDING_LEFT = 2
PADDING_TOP = 1


class TopBarWidget(BaseWidget):
    """A container widget for the players list and the pile widgets."""

    __slots__ = ("_players", "_pile")

    @property
    def height(self) -> int:
        return HEIGHT

    def __init__(
        self, pile: PileViewModel, players: tuple[PlayerViewModel, ...], theme: Theme
    ) -> None:
        self._players = PlayersListWidget(players=players, theme=theme)
        self._pile = PileWidget(viewmodel=pile, theme=theme)

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.render_widget(
            widget=self._players,
            position=Position.TOP,
            side=Side.LEFT,
            screen=screen,
            frame=frame,
            x_offset=PADDING_LEFT,
            y_offset=PADDING_TOP,
        )
        renderer.render_widget(
            widget=self._pile,
            position=Position.TOP,
            side=Side.RIGHT,
            screen=screen,
            frame=frame,
        )
        renderer.draw_separator(SeparatorSide.BOTTOM, frame, screen)
        renderer.set_background_color(Color.BG3, screen, frame)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TopBarWidget):
            return NotImplemented

        return self._players == other._players and self._pile == other._pile
