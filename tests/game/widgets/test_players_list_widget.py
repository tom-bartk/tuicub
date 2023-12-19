from unittest.mock import patch

import pytest

from src.tuicub.game.widgets.player import PlayerWidget
from src.tuicub.game.widgets.players_list import (
    HEIGHT,
    PADDING_LEFT,
    SPACING,
    PlayersListWidget,
)
from src.tuicub.game.widgets.renderer import HorizontalPosition


@pytest.fixture()
def sut(player_1_vm, player_2_vm, player_3_vm, theme) -> PlayersListWidget:
    return PlayersListWidget(players=(player_1_vm, player_2_vm, player_3_vm), theme=theme)


class TestRender:
    def test_renders_players_horizontally_from_left_to_right_with_spacing(
        self, sut, theme, renderer, screen, frame, player_1_vm, player_2_vm, player_3_vm
    ) -> None:
        player_1 = PlayerWidget(viewmodel=player_1_vm, theme=theme)
        player_2 = PlayerWidget(viewmodel=player_2_vm, theme=theme)
        player_3 = PlayerWidget(viewmodel=player_3_vm, theme=theme)

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_horizontally.assert_called_once_with(
            (player_1, player_2, player_3),
            HorizontalPosition.LEFT,
            frame,
            screen,
            spacing=SPACING,
        )


class TestHeight:
    def test_returns_correct_height(self, sut) -> None:
        expected = HEIGHT

        result = sut.height

        assert result == expected


class TestWidth:
    def test_returns_sum_of_players_widths_plus_spacing_and_left_padding(
        self, sut
    ) -> None:
        with patch(
            "prompt_toolkit.formatted_text.fragment_list_width", side_effect=[1, 2, 3]
        ):
            expected = (1 + SPACING) + (2 + SPACING) + (3 + SPACING) + PADDING_LEFT

            result = sut.width

            assert result == expected
