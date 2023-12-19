from prompt_toolkit.formatted_text import to_plain_text

from src.tuicub.common.strings import (
    GAME_STATUS_MOVE_MODE,
    GAME_STATUS_SELECT_MODE,
    GAME_STATUS_TURN_DONE,
)
from src.tuicub.common.views import Color
from src.tuicub.game.models import SelectionMode
from src.tuicub.game.viewmodels.status_bar import StatusBarViewModel


class TestBarBgColor:
    def test_when_has_no_turn__returns_color_bg5(self) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILES, has_turn=False)
        expected = Color.BG5

        result = sut.bar_bg_color()

        assert result == expected

    def test_when_has_turn__selection_tiles__returns_aqua_dim(self) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILES, has_turn=True)
        expected = Color.AQUA_DIM

        result = sut.bar_bg_color()

        assert result == expected

    def test_when_has_turn__selection_tilesets__returns_purple_dim(self) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILESETS, has_turn=True)
        expected = Color.PURPLE_DIM

        result = sut.bar_bg_color()

        assert result == expected


class TestContent:
    def test_when_has_no_turn__text_is_turn_done(self, theme) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILES, has_turn=False)
        expected = f" {GAME_STATUS_TURN_DONE} "

        result = to_plain_text(sut.content(theme=theme))

        assert result == expected

    def test_when_has_no_turn__fg_is_bg5__bg_is_gray(self, theme) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILES, has_turn=False)

        sut.content(theme=theme)

        theme.style.assert_called_once_with(fg=Color.BG5, bg=Color.GRAY, bold=True)

    def test_when_has_turn__selection_tiles__text_is_select_mode(self, theme) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILES, has_turn=True)
        expected = f" {GAME_STATUS_SELECT_MODE} "

        result = to_plain_text(sut.content(theme=theme))

        assert result == expected

    def test_when_has_turn__selection_tiles__fg_is_fg_black__bg_is_aqua(
        self, theme
    ) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILES, has_turn=True)

        sut.content(theme=theme)

        theme.style.assert_called_once_with(fg=Color.FG_BLACK, bg=Color.AQUA, bold=True)

    def test_when_has_turn__selection_tilesets__text_is_move_mode(self, theme) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILESETS, has_turn=True)
        expected = f" {GAME_STATUS_MOVE_MODE} "

        result = to_plain_text(sut.content(theme=theme))

        assert result == expected

    def test_when_has_turn__selection_tilesets__fg_is_fg_black__bg_is_purple(
        self, theme
    ) -> None:
        sut = StatusBarViewModel(selection_mode=SelectionMode.TILESETS, has_turn=True)

        sut.content(theme=theme)

        theme.style.assert_called_once_with(fg=Color.FG_BLACK, bg=Color.PURPLE, bold=True)
