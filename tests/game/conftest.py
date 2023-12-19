from collections.abc import Callable
from unittest.mock import create_autospec

import pytest
from prompt_toolkit.layout.screen import Screen
from pydepot import Store

from src.tuicub.common.models import Player
from src.tuicub.common.services.screen_size_service import ScreenSizeService
from src.tuicub.game.models import Tile, Tileset, VirtualTileset
from src.tuicub.game.state import GameScreenState
from src.tuicub.game.viewmodels.player import PlayerViewModel
from src.tuicub.game.viewmodels.tile import TileViewModel
from src.tuicub.game.viewmodels.tileset import TilesetViewModel
from src.tuicub.game.widgets.frame import Frame
from src.tuicub.game.widgets.renderer import Renderer


@pytest.fixture()
def renderer() -> Renderer:
    return create_autospec(Renderer)


@pytest.fixture()
def screen() -> Screen:
    return create_autospec(Screen)


@pytest.fixture()
def frame() -> Frame:
    return create_autospec(Frame)


@pytest.fixture()
def player_1_vm(player_1) -> PlayerViewModel:
    return PlayerViewModel(player=player_1)


@pytest.fixture()
def player_2_vm(player_2) -> PlayerViewModel:
    return PlayerViewModel(player=player_2)


@pytest.fixture()
def player_3_vm(player_3) -> PlayerViewModel:
    return PlayerViewModel(player=player_3)


@pytest.fixture()
def tile_vm(tile) -> Callable[[int, bool, bool, bool], TileViewModel]:
    def factory(
        tile_id: int,
        is_selected: bool = False,
        is_highlighted: bool = False,
        is_new: bool = False,
    ) -> TileViewModel:
        return TileViewModel(
            tile=tile(tile_id),
            is_selected=is_selected,
            is_highlighted=is_highlighted,
            is_new=is_new,
        )

    return factory


@pytest.fixture()
def tileset_vm(tileset) -> Callable[[...], TilesetViewModel]:
    def factory(
        *tiles: TileViewModel,
        is_highlighted: bool = False,
    ) -> TilesetViewModel:
        return TilesetViewModel(tiles=tiles, is_highlighted=is_highlighted)

    return factory


@pytest.fixture()
def tile() -> Callable[[int], Tile]:
    def factory(tile_id: int) -> Tile:
        return Tile.from_id(id=tile_id)

    return factory


@pytest.fixture()
def tileset() -> Callable[[[int, ...]], Tileset]:
    def factory(*tile_ids: int) -> Tileset:
        return Tileset.from_tile_ids(tiles=list(tile_ids))

    return factory


@pytest.fixture()
def virtual_tileset() -> Callable[[[int, ...]], VirtualTileset]:
    def factory(*tile_ids: int) -> VirtualTileset:
        return VirtualTileset(tiles=tuple(Tile.from_id(tile) for tile in tile_ids))

    return factory


@pytest.fixture()
def player_1(user_1) -> Player:
    return Player(user_id=user_1.id, name=user_1.name, tiles_count=13, has_turn=True)


@pytest.fixture()
def player_2(user_2) -> Player:
    return Player(user_id=user_2.id, name=user_2.name, tiles_count=7, has_turn=False)


@pytest.fixture()
def player_3(user_3) -> Player:
    return Player(user_id=user_3.id, name=user_3.name, tiles_count=42, has_turn=False)


@pytest.fixture()
def player(player_1) -> Player:
    return player_1


@pytest.fixture()
def local_store() -> Store[GameScreenState]:
    return create_autospec(Store)


@pytest.fixture()
def screen_size_service() -> ScreenSizeService:
    return create_autospec(ScreenSizeService)
