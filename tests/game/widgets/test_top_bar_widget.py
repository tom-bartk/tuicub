from unittest.mock import create_autospec

import pytest

from src.tuicub.common.views import Color
from src.tuicub.game.viewmodels.pile import PileViewModel
from src.tuicub.game.widgets.pile import PileWidget
from src.tuicub.game.widgets.players_list import PlayersListWidget
from src.tuicub.game.widgets.renderer import Position, SeparatorSide, Side
from src.tuicub.game.widgets.top_bar import (
    HEIGHT,
    PADDING_LEFT,
    PADDING_TOP,
    TopBarWidget,
)


@pytest.fixture()
def pile_vm() -> PileViewModel:
    return create_autospec(PileViewModel)


@pytest.fixture()
def sut(pile_vm, player_1_vm, player_2_vm, player_3_vm, theme) -> TopBarWidget:
    return TopBarWidget(
        pile=pile_vm, players=(player_1_vm, player_2_vm, player_3_vm), theme=theme
    )


class TestRender:
    def test_renders_playrs_list_widget_at_top_left(
        self, sut, theme, renderer, screen, frame, player_1_vm, player_2_vm, player_3_vm
    ) -> None:
        players_list = PlayersListWidget(
            players=(player_1_vm, player_2_vm, player_3_vm), theme=theme
        )

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_widget.assert_any_call(
            widget=players_list,
            position=Position.TOP,
            side=Side.LEFT,
            screen=screen,
            frame=frame,
            x_offset=PADDING_LEFT,
            y_offset=PADDING_TOP,
        )

    def test_renders_pile_widget_at_top_right(
        self, sut, theme, renderer, screen, frame, pile_vm
    ) -> None:
        pile = PileWidget(viewmodel=pile_vm, theme=theme)

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_widget.assert_any_call(
            widget=pile,
            position=Position.TOP,
            side=Side.RIGHT,
            screen=screen,
            frame=frame,
        )

    def test_draws_bottom_separator(self, sut, screen, frame, renderer) -> None:
        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.draw_separator.assert_called_once_with(
            SeparatorSide.BOTTOM, frame, screen
        )

    def test_sets_background_color_to_bg3(self, sut, screen, frame, renderer) -> None:
        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.set_background_color.assert_called_once_with(Color.BG3, screen, frame)


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = HEIGHT

        result = sut.height

        assert result == expected
