from prompt_toolkit.layout.screen import Screen

from ...common.views import Theme
from ..viewmodels.player import PlayerViewModel
from .base import BaseWidget
from .frame import Frame
from .player import PlayerWidget
from .renderer import HorizontalPosition, Renderer

PADDING_LEFT = 2
SPACING = 2
HEIGHT = 1


class PlayersListWidget(BaseWidget):
    """A widget displaying the list of all players in the game."""

    __slots__ = ("_players",)

    @property
    def width(self) -> int:
        return (
            sum(tuple(player.width + SPACING for player in self._players)) + PADDING_LEFT
        )

    @property
    def height(self) -> int:
        return HEIGHT

    def __init__(self, players: tuple[PlayerViewModel, ...], theme: Theme) -> None:
        self._players = tuple(
            PlayerWidget(viewmodel=player, theme=theme) for player in players
        )

    def render(self, renderer: Renderer, screen: Screen, frame: Frame) -> None:
        renderer.render_horizontally(
            self._players, HorizontalPosition.LEFT, frame, screen, spacing=SPACING
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlayersListWidget):
            return NotImplemented

        return self._players == other._players
