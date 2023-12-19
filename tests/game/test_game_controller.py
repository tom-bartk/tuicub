from unittest.mock import create_autospec

import pytest

from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.state import FinishGameAction
from src.tuicub.common.strings import GAME_NO_TILES_SELECTED_ALERT
from src.tuicub.game.actions import (
    SetTilesetsSelectionAction,
    SetTilesSelectionAction,
    ToggleTileSelectedAction,
)
from src.tuicub.game.controller import GameController
from src.tuicub.game.interactors.actions import ActionsInteractor
from src.tuicub.game.interactors.scroll import ScrollInteractor
from src.tuicub.game.models import ScrollDirection
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def actions_interactor() -> ActionsInteractor:
    return create_autospec(ActionsInteractor)


@pytest.fixture()
def scroll_interactor() -> ScrollInteractor:
    return create_autospec(ScrollInteractor)


@pytest.fixture()
def sut(
    store,
    actions_interactor,
    scroll_interactor,
    alert_service,
    local_store,
) -> GameController:
    return GameController(
        actions_interactor=actions_interactor,
        alert_service=alert_service,
        local_store=local_store,
        scroll_interactor=scroll_interactor,
        store=store,
    )


class TestScroll:
    def test_calls_scroll_interactor_with_direction(self, sut, scroll_interactor) -> None:
        sut.scroll(ScrollDirection.RIGHT)

        scroll_interactor.scroll.assert_called_once_with(direction=ScrollDirection.RIGHT)


class TestToggleTileSelected:
    def test_dispatches_toggle_tile_selected_action_to_local_store(
        self, sut, event, local_store
    ) -> None:
        expected = ToggleTileSelectedAction()

        sut.toggle_tile_selected(event)

        local_store.dispatch.assert_called_once_with(expected)


class TestSetTilesSelection:
    def test_dispatches_set_tiles_selection_action_to_local_store(
        self, sut, event, local_store
    ) -> None:
        expected = SetTilesSelectionAction()

        sut.set_tiles_selection(event)

        local_store.dispatch.assert_called_once_with(expected)


class TestSetTilesetsSelection:
    def test_when_no_selected_tiles__queues_no_tiles_selected_alert(
        self, sut, event, local_store, alert_service
    ) -> None:
        local_store.state = GameScreenState(selected_tiles=frozenset())
        expected = Alert(GAME_NO_TILES_SELECTED_ALERT, AlertType.WARNING)

        sut.set_tilesets_selection(event)

        alert_service.queue_alert.assert_called_once_with(expected)
        local_store.dispatch.assert_not_called()

    def test_when_has_selected_tiles__dispatches_set_tilesets_selection_action(
        self, sut, event, local_store, alert_service, tile
    ) -> None:
        local_store.state = GameScreenState(selected_tiles=frozenset({tile(1), tile(2)}))
        expected = SetTilesetsSelectionAction()

        sut.set_tilesets_selection(event)

        local_store.dispatch.assert_called_once_with(expected)
        alert_service.queue_alert.assert_not_called()


class TestMoveTiles:
    def test_calls_move_tiles_on_actions_interactor(
        self, sut, event, actions_interactor
    ) -> None:
        sut.move_tiles(event)

        actions_interactor.move_tiles.assert_called_once()


class TestUndo:
    def test_calls_undo_on_actions_interactor(
        self, sut, event, actions_interactor
    ) -> None:
        sut.undo(event)

        actions_interactor.undo.assert_called_once()


class TestRedo:
    def test_calls_redo_on_actions_interactor(
        self, sut, event, actions_interactor
    ) -> None:
        sut.redo(event)

        actions_interactor.redo.assert_called_once()


class TestEndTurn:
    def test_calls_end_turn_on_actions_interactor(
        self, sut, event, actions_interactor
    ) -> None:
        sut.end_turn(event)

        actions_interactor.end_turn.assert_called_once()


class TestDraw:
    def test_calls_draw_on_actions_interactor(
        self, sut, event, actions_interactor
    ) -> None:
        sut.draw(event)

        actions_interactor.draw.assert_called_once()


class TestFinishGame:
    def test_dispatches_finish_game_action_to_global_store(
        self, sut, event, store
    ) -> None:
        expected = FinishGameAction()

        sut.finish_game(event)

        store.dispatch.assert_called_once_with(expected)
