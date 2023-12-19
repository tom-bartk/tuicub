from unittest.mock import Mock, create_autospec

import pytest

from src.tuicub.game.actions import SetHighlightedTileAction, SetHighlightedTilesetAction
from src.tuicub.game.interactors.scroll import ScrollInteractor
from src.tuicub.game.models import ScrollDirection, SelectionMode
from src.tuicub.game.services.scroll_service import ScrollService
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def scroll_service() -> ScrollService:
    return create_autospec(ScrollService)


@pytest.fixture()
def sut(local_store, scroll_service) -> ScrollInteractor:
    return ScrollInteractor(scroll_service=scroll_service, store=local_store)


class TestScroll:
    def test_when_selection_tiles__service_returns_tile__dispatches_set_highlighted_tile(
        self, sut, scroll_service, local_store, tile
    ) -> None:
        local_store.state = GameScreenState(selection_mode=SelectionMode.TILES)
        scroll_service.scroll_tiles = Mock(return_value=tile(42))
        expected = SetHighlightedTileAction(tile=tile(42))

        sut.scroll(direction=ScrollDirection.UP)

        local_store.dispatch.assert_called_once_with(expected)

    def test_when_selection_tiles__service_returns_none__does_not_dispatch(
        self, sut, scroll_service, local_store, tile
    ) -> None:
        local_store.state = GameScreenState(selection_mode=SelectionMode.TILES)
        scroll_service.scroll_tiles = Mock(return_value=None)

        sut.scroll(direction=ScrollDirection.UP)

        local_store.dispatch.assert_not_called()

    def test_when_selection_tilesets__service_returns_tileset__dispatches_set_highlighted_tileset(  # noqa: E501
        self, sut, scroll_service, local_store, tileset
    ) -> None:
        local_store.state = GameScreenState(selection_mode=SelectionMode.TILESETS)
        scroll_service.scroll_tilesets = Mock(return_value=tileset(1, 2, 3))
        expected = SetHighlightedTilesetAction(tileset=tileset(1, 2, 3))

        sut.scroll(direction=ScrollDirection.UP)

        local_store.dispatch.assert_called_once_with(expected)

    def test_when_selection_tilesets__service_returns_none__does_not_dispatch(
        self, sut, scroll_service, local_store, tileset
    ) -> None:
        local_store.state = GameScreenState(selection_mode=SelectionMode.TILESETS)
        scroll_service.scroll_tilesets = Mock(return_value=None)

        sut.scroll(direction=ScrollDirection.UP)

        local_store.dispatch.assert_not_called()
