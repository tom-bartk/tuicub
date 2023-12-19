from unittest.mock import call

from prompt_toolkit.formatted_text import to_plain_text

from src.tuicub.common.strings import GAME_TILE_ICON_2
from src.tuicub.common.views import Color
from src.tuicub.game.viewmodels.player import PlayerViewModel


class TestContent:
    def test_text_has_player_name_and_tiles_count(self, theme, player) -> None:
        sut = PlayerViewModel(player=player)
        expected = f" {player.name} Ⅰ{GAME_TILE_ICON_2} {player.tiles_count} "

        result = to_plain_text(sut.content(theme=theme))

        assert result == expected

    def test_when_has_turn__is_bold__fg_is_fg0__bg_is_green_dark(
        self, theme, player
    ) -> None:
        sut = PlayerViewModel(player=player)
        expected = [
            call(fg=Color.FG0, bg=Color.GREEN_DARK, bold=True),
            call(fg=Color.GREEN, bg=Color.GREEN_DARK),
            call(fg=Color.FG0, bg=Color.GREEN_DARK),
        ]

        sut.content(theme=theme)

        theme.style.assert_has_calls(expected)

    def test_when_has_no_turn__is_not_bold__fg_is_fg2__bg_is_bg7(
        self, theme, player_2
    ) -> None:
        sut = PlayerViewModel(player=player_2)
        expected = [
            call(fg=Color.FG2, bg=Color.BG7, bold=False),
            call(fg=Color.FG5, bg=Color.BG7),
            call(fg=Color.FG2, bg=Color.BG7),
        ]

        sut.content(theme=theme)

        theme.style.assert_has_calls(expected)
