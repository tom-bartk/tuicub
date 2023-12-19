from collections.abc import Callable
from unittest.mock import create_autospec

import pytest
from pydepot import Store

from src.tuicub.common.models import Player
from src.tuicub.game.models import SelectionMode
from src.tuicub.game.services.board_service import BoardService
from src.tuicub.game.services.scroll_service import ScrollService
from src.tuicub.game.state import GameScreenState
from src.tuicub.game.viewmodel import GameViewModel
from src.tuicub.game.viewmodels.pile import PileViewModel
from src.tuicub.game.viewmodels.player import PlayerViewModel
from src.tuicub.game.viewmodels.status_bar import StatusBarViewModel
from src.tuicub.game.viewmodels.tile import TileViewModel, VirtualTileViewModel
from src.tuicub.game.viewmodels.tileset import TilesetViewModel
from src.tuicub.game.viewmodels.winner import WinnerViewModel


@pytest.fixture()
def virtual_tile_vm(tile) -> Callable[[int, bool, bool, bool], VirtualTileViewModel]:
    def factory(
        tile_id: int,
        is_selected: bool = False,
        is_highlighted: bool = False,
        is_new: bool = False,
    ) -> VirtualTileViewModel:
        return VirtualTileViewModel(
            tile=tile(tile_id),
            is_selected=is_selected,
            is_highlighted=is_highlighted,
            is_new=is_new,
        )

    return factory


@pytest.fixture()
def virtual_tileset_vm(tileset) -> Callable[[...], TilesetViewModel]:
    def factory(
        *tiles: TileViewModel,
        is_highlighted: bool = False,
    ) -> TilesetViewModel:
        return TilesetViewModel(tiles=tiles, is_highlighted=is_highlighted)

    return factory


@pytest.fixture()
def scroll_service() -> ScrollService:
    return create_autospec(ScrollService)


@pytest.fixture()
def board_service() -> BoardService:
    return create_autospec(BoardService)


@pytest.fixture()
def store(local_store) -> Store[GameScreenState]:
    return local_store


@pytest.fixture()
def sut(
    board_service, scroll_service, store, user_id_1, events_observer
) -> GameViewModel:
    return GameViewModel(
        board_service=board_service,
        events_observer=events_observer,
        scroll_service=scroll_service,
        store=store,
        user_id=user_id_1,
    )


class TestBoard:
    def test_when_selection_tiles__tile_vm_highlighted(
        self, sut, board_service, tileset, tile, tile_vm, tileset_vm
    ) -> None:
        board = (
            (tileset(1, 2, 3), tileset(4, 5, 6)),
            (tileset(7, 8, 9),),
        )
        new_tiles = frozenset([tile(1), tile(9)])
        highlighted_tile = tile(2)
        selected_tiles = frozenset([tile(2), tile(4), tile(7)])
        board_service.create_rows.return_value = board
        expected = (
            (
                tileset_vm(
                    tile_vm(1, is_new=True),
                    tile_vm(2, is_highlighted=True, is_selected=True),
                    tile_vm(3),
                ),
                tileset_vm(tile_vm(4, is_selected=True), tile_vm(5), tile_vm(6)),
            ),
            (
                tileset_vm(
                    tile_vm(7, is_selected=True), tile_vm(8), tile_vm(9, is_new=True)
                ),
            ),
        )
        sut.on_state(
            GameScreenState(
                new_tiles=new_tiles,
                highlighted_tile=highlighted_tile,
                selected_tiles=selected_tiles,
                selection_mode=SelectionMode.TILES,
            )
        )
        result = sut.board

        assert result == expected

    def test_when_selection_tilesets__tile_vm_not_highlighted__virtual_tileset_highlighted(  # noqa: E501
        self,
        sut,
        board_service,
        tileset,
        tile,
        tile_vm,
        tileset_vm,
        virtual_tileset_vm,
        virtual_tile_vm,
        virtual_tileset,
    ) -> None:
        board = (
            (tileset(1, 2, 3), tileset(4, 5, 6)),
            (tileset(7, 8, 9),),
        )
        new_tiles = frozenset([tile(1), tile(9)])
        highlighted_tile = tile(2)
        selected_tiles = frozenset([tile(2), tile(4), tile(7)])
        board_service.create_rows.return_value = board
        expected = (
            (
                tileset_vm(
                    tile_vm(1, is_new=True),
                    tile_vm(2, is_highlighted=False, is_selected=True),
                    tile_vm(3),
                ),
                tileset_vm(tile_vm(4, is_selected=True), tile_vm(5), tile_vm(6)),
            ),
            (
                tileset_vm(
                    tile_vm(7, is_selected=True), tile_vm(8), tile_vm(9, is_new=True)
                ),
            ),
            (
                virtual_tileset_vm(
                    virtual_tile_vm(2, is_selected=True),
                    virtual_tile_vm(4, is_selected=True),
                    virtual_tile_vm(7, is_selected=True),
                    is_highlighted=True,
                ),
            ),
        )

        sut.on_state(
            GameScreenState(
                new_tiles=new_tiles,
                highlighted_tile=highlighted_tile,
                highlighted_tileset=virtual_tileset(2, 4, 7),
                selected_tiles=selected_tiles,
                selection_mode=SelectionMode.TILESETS,
                virtual_tileset=virtual_tileset(2, 4, 7),
            )
        )
        result = sut.board

        assert result == expected


class TestPlayers:
    def test_returns_viewmodels_for_players_from_state(
        self, sut, player_1, player_2, player_3
    ) -> None:
        expected = (
            PlayerViewModel(player=player_1),
            PlayerViewModel(player=player_2),
            PlayerViewModel(player=player_3),
        )

        sut.on_state(GameScreenState(players=(player_1, player_2, player_3)))
        result = sut.players

        assert result == expected


class TestRack:
    def test_when_selection_tiles__tile_vm_highlighted(
        self, sut, tileset, tile, tile_vm, tileset_vm
    ) -> None:
        rack = tileset(1, 2, 3, 4, 5)
        new_tiles = frozenset([tile(5)])
        highlighted_tile = tile(4)
        selected_tiles = frozenset([tile(2), tile(3)])
        expected = tileset_vm(
            tile_vm(1),
            tile_vm(2, is_selected=True),
            tile_vm(3, is_selected=True),
            tile_vm(4, is_highlighted=True),
            tile_vm(5, is_new=True),
        )

        sut.on_state(
            GameScreenState(
                rack=rack,
                new_tiles=new_tiles,
                highlighted_tile=highlighted_tile,
                selected_tiles=selected_tiles,
                selection_mode=SelectionMode.TILES,
            )
        )
        result = sut.rack

        assert result == expected

    def test_when_selection_tilesets__tile_vm_not_highlighted(
        self, sut, tileset, tile, tile_vm, tileset_vm
    ) -> None:
        rack = tileset(1, 2, 3, 4, 5)
        new_tiles = frozenset([tile(5)])
        highlighted_tile = tile(4)
        selected_tiles = frozenset([tile(2), tile(3)])
        expected = tileset_vm(
            tile_vm(1),
            tile_vm(2, is_selected=True),
            tile_vm(3, is_selected=True),
            tile_vm(4, is_highlighted=False),
            tile_vm(5, is_new=True),
        )

        sut.on_state(
            GameScreenState(
                rack=rack,
                new_tiles=new_tiles,
                highlighted_tile=highlighted_tile,
                selected_tiles=selected_tiles,
                selection_mode=SelectionMode.TILESETS,
            )
        )
        result = sut.rack

        assert result == expected


class TestPile:
    def test_returns_pile_viewmodel_with_pile_count_from_state(self, sut) -> None:
        expected = PileViewModel(pile_count=42)

        sut.on_state(GameScreenState(pile_count=42))
        result = sut.pile

        assert result == expected


class TestWinner:
    def test_when_state_has_no_winner__returns_none(self, sut) -> None:
        expected = None

        sut.on_state(GameScreenState(winner=None))
        result = sut.winner

        assert result == expected

    def test_when_state_has_winner__returns_winner_viewmodel(self, sut, player_1) -> None:
        expected = WinnerViewModel(winner=player_1)

        sut.on_state(GameScreenState(winner=player_1))
        result = sut.winner

        assert result == expected


class TestStatusBar:
    def test_when_player_has_turn__viewmodel_has_turn(
        self, sut, user_1, player_2, player_3
    ) -> None:
        players = (
            Player(user_id=user_1.id, name=user_1.name, tiles_count=13, has_turn=True),
            player_2,
            player_3,
        )
        expected = StatusBarViewModel(selection_mode=SelectionMode.TILES, has_turn=True)

        sut.on_state(GameScreenState(players=players, selection_mode=SelectionMode.TILES))
        result = sut.status_bar

        assert result == expected

    def test_when_player_has_no_turn__viewmodel_has_no_turn(
        self, sut, user_1, player_2, player_3
    ) -> None:
        players = (
            Player(user_id=user_1.id, name=user_1.name, tiles_count=13, has_turn=False),
            player_2,
            player_3,
        )
        expected = StatusBarViewModel(
            selection_mode=SelectionMode.TILESETS, has_turn=False
        )

        sut.on_state(
            GameScreenState(players=players, selection_mode=SelectionMode.TILESETS)
        )
        result = sut.status_bar

        assert result == expected


class TestSubscribe:
    def test_subscribes_to_store_and_starts_events_observer(
        self, sut, store, events_observer
    ) -> None:
        sut.subscribe()

        store.subscribe.assert_called_once_with(sut, include_current=True)
        events_observer.observe.assert_called_once()


class TestUnsubscribe:
    def test_unsubscribes_from_store_and_stops_events_observer(
        self, sut, store, events_observer
    ) -> None:
        sut.unsubscribe()

        store.unsubscribe.assert_called_once_with(sut)
        events_observer.stop.assert_called_once()
