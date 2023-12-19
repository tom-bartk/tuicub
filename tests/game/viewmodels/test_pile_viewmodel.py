from prompt_toolkit.formatted_text import to_plain_text

from src.tuicub.common.strings import GAME_TILE_ICON_2
from src.tuicub.common.views import Color
from src.tuicub.game.viewmodels.pile import PileViewModel


class TestContent:
    def test_text_is_icon_and_pile_count_justified_by_3(self, theme) -> None:
        sut = PileViewModel(pile_count=7)
        expected = f"\n  {GAME_TILE_ICON_2} {str(7).ljust(3)} "

        result = to_plain_text(sut.content(theme=theme))

        assert result == expected

    def test_fg_is_fg1__bg_is_bg7__bold(self, theme) -> None:
        sut = PileViewModel(pile_count=7)

        sut.content(theme=theme)

        theme.style.assert_called_once_with(fg=Color.FG1, bg=Color.BG7, bold=True)
