from collections.abc import Callable
from unittest.mock import call, create_autospec

import pytest

from src.tuicub.common.views import Color
from src.tuicub.game.viewmodels.pile import PileViewModel
from src.tuicub.game.viewmodels.player import PlayerViewModel
from src.tuicub.game.viewmodels.status_bar import StatusBarViewModel
from src.tuicub.game.viewmodels.tileset import TilesetViewModel
from src.tuicub.game.viewmodels.winner import WinnerViewModel
from src.tuicub.game.widgets.board import BoardWidget
from src.tuicub.game.widgets.game import GameWidget
from src.tuicub.game.widgets.rack import RackWidget
from src.tuicub.game.widgets.renderer import Position, Side
from src.tuicub.game.widgets.status_bar import StatusBarWidget
from src.tuicub.game.widgets.top_bar import TopBarWidget
from src.tuicub.game.widgets.winner import WinnerWidget


@pytest.fixture()
def pile_vm() -> PileViewModel:
    return create_autospec(PileViewModel)


@pytest.fixture()
def status_bar_vm() -> StatusBarViewModel:
    return create_autospec(StatusBarViewModel)


@pytest.fixture()
def winner_vm() -> WinnerViewModel:
    return create_autospec(WinnerViewModel)


@pytest.fixture()
def rack_vm(tileset_vm, tile_vm) -> TilesetViewModel:
    return tileset_vm(tile_vm(1), tile_vm(2), tile_vm(3))


@pytest.fixture()
def board(tileset_vm, tile_vm) -> tuple[tuple[TilesetViewModel, ...], ...]:
    return (
        (
            tileset_vm(tile_vm(1), tile_vm(2), tile_vm(3)),
            tileset_vm(tile_vm(4), tile_vm(5), tile_vm(6)),
        ),
        (tileset_vm(tile_vm(7), tile_vm(8), tile_vm(9)),),
    )


@pytest.fixture()
def players(player_1_vm, player_2_vm, player_3_vm) -> tuple[PlayerViewModel, ...]:
    return (player_1_vm, player_2_vm, player_3_vm)


@pytest.fixture()
def create_sut(
    pile_vm, board, rack_vm, status_bar_vm, players, theme
) -> Callable[[WinnerViewModel | None], GameWidget]:
    def factory(winner: WinnerViewModel | None = None) -> GameWidget:
        return GameWidget(
            board=board,
            rack=rack_vm,
            pile=pile_vm,
            players=players,
            status_bar=status_bar_vm,
            winner=winner,
            theme=theme,
        )

    return factory


class TestRender:
    def test_when_no_winner__renders_top_bar_status_bar_rack_and_board(
        self,
        create_sut,
        theme,
        renderer,
        screen,
        frame,
        players,
        rack_vm,
        board,
        status_bar_vm,
        pile_vm,
    ) -> None:
        rack = RackWidget(viewmodel=rack_vm, theme=theme)
        board = BoardWidget(board=board, theme=theme)
        status_bar = StatusBarWidget(viewmodel=status_bar_vm, theme=theme)
        top_bar = TopBarWidget(pile=pile_vm, players=players, theme=theme)
        expected_calls = [
            call(
                widget=status_bar,
                position=Position.BOTTOM,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
            ),
            call(
                widget=rack,
                position=Position.BOTTOM,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
                y_offset=status_bar.height,
            ),
            call(
                widget=board,
                position=Position.TOP,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
                height=frame.height - (top_bar.height + rack.height),
                y_offset=top_bar.height,
            ),
            call(
                widget=top_bar,
                position=Position.TOP,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
            ),
        ]
        sut = create_sut(winner=None)

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_widget.assert_has_calls(expected_calls)

    def test_when_winner__renders_top_bar_and_winner(
        self, create_sut, theme, renderer, screen, frame, players, pile_vm, winner_vm
    ) -> None:
        winner = WinnerWidget(viewmodel=winner_vm, theme=theme)
        top_bar = TopBarWidget(pile=pile_vm, players=players, theme=theme)
        expected_calls = [
            call(
                widget=winner,
                position=Position.CENTER,
                side=Side.CENTER,
                screen=screen,
                frame=frame,
                width=winner.width,
            ),
            call(
                widget=top_bar,
                position=Position.TOP,
                side=Side.LEFT,
                screen=screen,
                frame=frame,
                width=frame.width,
            ),
        ]
        sut = create_sut(winner=winner_vm)

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.render_widget.assert_has_calls(expected_calls)

    def test_sets_background_color_to_bg2(
        self, create_sut, screen, frame, renderer
    ) -> None:
        sut = create_sut()

        sut.render(renderer=renderer, screen=screen, frame=frame)

        renderer.set_background_color.assert_called_once_with(Color.BG2, screen, frame)
