from pydepot import Store

from ..actions import SetHighlightedTileAction, SetHighlightedTilesetAction
from ..models import ScrollDirection, SelectionMode
from ..services.scroll_service import ScrollService
from ..state import GameScreenState


class ScrollInteractor:
    """Interactor for scrolling the game board."""

    __slots__ = ("_scroll_service", "_store")

    def __init__(self, scroll_service: ScrollService, store: Store[GameScreenState]):
        self._scroll_service: ScrollService = scroll_service
        self._store: Store[GameScreenState] = store

    def scroll(self, direction: ScrollDirection) -> None:
        """Scroll the game board in the given direction.

        Scrolls tiles if the selection mode is tiles, otherwise scrolls tilesets.
        Scrolling means changing the currently highlighted tile/tileset
        to the next one based on the direction of the scroll.

        Args:
            direction (ScrollDirection): The scrolling direction.
        """
        if self._store.state.selection_mode == SelectionMode.TILES:
            self._scroll_tiles(direction=direction)
        else:
            self._scroll_tilesets(direction=direction)

    def _scroll_tiles(self, direction: ScrollDirection) -> None:
        if tile := self._scroll_service.scroll_tiles(
            direction=direction, state=self._store.state
        ):
            self._store.dispatch(action=SetHighlightedTileAction(tile=tile))

    def _scroll_tilesets(self, direction: ScrollDirection) -> None:
        if tileset := self._scroll_service.scroll_tilesets(
            direction=direction, state=self._store.state
        ):
            self._store.dispatch(action=SetHighlightedTilesetAction(tileset=tileset))
