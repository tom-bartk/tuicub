from collections.abc import Callable
from unittest.mock import create_autospec

import pytest

from src.tuicub.common.models import Keybind, Player
from src.tuicub.common.state import State
from src.tuicub.common.strings import (
    ARROW_LEFT,
    ARROW_RIGHT,
    ARROW_UP,
    ARROWS_ALL,
    GAME_DRAW_KEY_TOOLTIP,
    GAME_END_TURN_KEY_TOOLTIP,
    GAME_FINISH_GAME_KEY_TOOLTIP,
    GAME_MOVE_MODE_KEY_TOOLTIP,
    GAME_MOVE_TILES_KEY_TOOLTIP,
    GAME_REDO_KEY_TOOLTIP,
    GAME_SELECT_MODE_KEY_TOOLTIP,
    GAME_TOGGLE_SELECTED_KEY_TOOLTIP,
    GAME_UNDO_KEY_TOOLTIP,
)
from src.tuicub.game.controller import GameController
from src.tuicub.game.keybinds import (
    GameKeybindsContainer,
    HasTurnNoWinner,
    HasTurnNoWinnerTilesetsSelectionMode,
    HasTurnNoWinnerTilesSelectionMode,
    HasWinner,
)
from src.tuicub.game.models import ScrollDirection, SelectionMode
from src.tuicub.game.state import GameScreenState


@pytest.fixture()
def controller() -> GameController:
    return create_autospec(GameController)


@pytest.fixture()
def state(user_1) -> Callable[[bool, bool], GameScreenState]:
    def factory(
        has_turn: bool = True,
        has_winner: bool = False,
        selection_mode: SelectionMode = SelectionMode.TILES,
    ) -> GameScreenState:
        player = Player(
            user_id=user_1.id, name=user_1.name, tiles_count=42, has_turn=has_turn
        )
        return GameScreenState(
            players=(player,),
            winner=player if has_winner else None,
            selection_mode=selection_mode,
        )

    return factory


@pytest.fixture()
def sut(controller, local_store, store, app_store, user_1) -> GameKeybindsContainer:
    store.state = State(current_user=user_1)
    return GameKeybindsContainer(
        controller=controller, store=store, local_store=local_store, app_store=app_store
    )


class TestKeybinds:
    def test_returns_correct_keybinds(self, sut, controller) -> None:
        expected = [
            Keybind(
                key=("h", "left"),
                display_key="h",
                tooltip=ARROW_LEFT,
                action=lambda _: controller.scroll(ScrollDirection.LEFT),
                is_hidden=True,
            ),
            Keybind(
                key=("j", "down"),
                display_key="hjkl",
                tooltip=ARROWS_ALL,
                action=lambda _: controller.scroll(ScrollDirection.DOWN),
                is_hidden=False,
            ),
            Keybind(
                key="k",
                display_key="k",
                tooltip=ARROW_UP,
                action=lambda _: controller.scroll(ScrollDirection.UP),
                is_hidden=True,
            ),
            Keybind(
                key=("l", "right"),
                display_key="k",
                tooltip=ARROW_RIGHT,
                action=lambda _: controller.scroll(ScrollDirection.RIGHT),
                is_hidden=True,
            ),
            Keybind(
                key="u",
                display_key="u",
                tooltip=GAME_UNDO_KEY_TOOLTIP,
                action=controller.undo,
            ),
            Keybind(
                key="r",
                display_key="r",
                tooltip=GAME_REDO_KEY_TOOLTIP,
                action=controller.redo,
            ),
            Keybind(
                key="e",
                display_key="e",
                tooltip=GAME_END_TURN_KEY_TOOLTIP,
                action=controller.end_turn,
            ),
            Keybind(
                key="d",
                display_key="d",
                tooltip=GAME_DRAW_KEY_TOOLTIP,
                action=controller.draw,
            ),
            Keybind(
                key="s",
                display_key="s",
                tooltip=GAME_SELECT_MODE_KEY_TOOLTIP,
                action=controller.set_tiles_selection,
            ),
            Keybind(
                key="m",
                display_key="m",
                tooltip=GAME_MOVE_MODE_KEY_TOOLTIP,
                action=controller.set_tilesets_selection,
            ),
            Keybind(
                key="space",
                display_key="space",
                tooltip=GAME_TOGGLE_SELECTED_KEY_TOOLTIP,
                action=controller.toggle_tile_selected,
            ),
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=GAME_MOVE_TILES_KEY_TOOLTIP,
                action=controller.move_tiles,
            ),
            Keybind(
                key="c-m",
                display_key="enter",
                tooltip=GAME_FINISH_GAME_KEY_TOOLTIP,
                action=controller.finish_game,
            ),
        ]

        result = sut.keybinds()

        assert result == expected

    def test_scroll_left__scrolls_left(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[0]

        keybind.action(event)

        controller.scroll.assert_called_once_with(ScrollDirection.LEFT)

    def test_scroll_left__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[0]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_scroll_down__scrolls_down(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[1]

        keybind.action(event)

        controller.scroll.assert_called_once_with(ScrollDirection.DOWN)

    def test_scroll_down__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[1]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_scroll_up__scrolls_up(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[2]

        keybind.action(event)

        controller.scroll.assert_called_once_with(ScrollDirection.UP)

    def test_scroll_up__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[2]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_scroll_right__scrolls_right(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[3]

        keybind.action(event)

        controller.scroll.assert_called_once_with(ScrollDirection.RIGHT)

    def test_scroll_right__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[3]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_undo_undos(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[4]

        keybind.action(event)

        controller.undo.assert_called_once()

    def test_undo__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[4]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_redo_redos(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[5]

        keybind.action(event)

        controller.redo.assert_called_once()

    def test_redo__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[5]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_end_turn__ends_turn(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[6]

        keybind.action(event)

        controller.end_turn.assert_called_once()

    def test_end_turn__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[6]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_draw__draws(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[7]

        keybind.action(event)

        controller.draw.assert_called_once()

    def test_draw__condition_is_has_turn_no_winner(self, sut) -> None:
        keybind = sut.keybinds()[7]

        assert isinstance(keybind.condition, HasTurnNoWinner)

    def test_select_mode__sets_tiles_selection(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[8]

        keybind.action(event)

        controller.set_tiles_selection.assert_called_once()

    def test_select_mode__condition_is_has_turn_no_winner_tilesets_selection(
        self, sut
    ) -> None:
        keybind = sut.keybinds()[8]

        assert isinstance(keybind.condition, HasTurnNoWinnerTilesetsSelectionMode)

    def test_move_mode__sets_tilesets_selection(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[9]

        keybind.action(event)

        controller.set_tilesets_selection.assert_called_once()

    def test_move_mode__condition_is_has_turn_no_winner_tiles_selection(
        self, sut
    ) -> None:
        keybind = sut.keybinds()[9]

        assert isinstance(keybind.condition, HasTurnNoWinnerTilesSelectionMode)

    def test_toggle_selected__toggles_selected_tile(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[10]

        keybind.action(event)

        controller.toggle_tile_selected.assert_called_once()

    def test_toggle_selected__condition_is_has_turn_no_winner_tiles_selection(
        self, sut
    ) -> None:
        keybind = sut.keybinds()[10]

        assert isinstance(keybind.condition, HasTurnNoWinnerTilesSelectionMode)

    def test_move_tiles__moves_tiles(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[11]

        keybind.action(event)

        controller.move_tiles.assert_called_once()

    def test_move_tiles__condition_is_has_turn_no_winner_tilesets_selection(
        self, sut
    ) -> None:
        keybind = sut.keybinds()[11]

        assert isinstance(keybind.condition, HasTurnNoWinnerTilesetsSelectionMode)

    def test_finish_game__finishes_game(self, sut, event, controller) -> None:
        keybind = sut.keybinds()[12]

        keybind.action(event)

        controller.finish_game.assert_called_once()

    def test_move_tiles__condition_is_has_winner(self, sut) -> None:
        keybind = sut.keybinds()[12]

        assert isinstance(keybind.condition, HasWinner)


class TestHasTurnNoWinner:
    @pytest.fixture()
    def sut(self, store, user_1, local_store) -> HasTurnNoWinner:
        store.state = State(current_user=user_1)
        return HasTurnNoWinner(store=store, local_store=local_store)

    def test_when_has_turn__no_winner__is_true(self, sut, state, local_store) -> None:
        local_store.state = state(has_turn=True, has_winner=False)
        expected = True

        result = sut()

        assert result == expected

    def test_when_has_turn__has_winner__is_false(self, sut, state, local_store) -> None:
        local_store.state = state(has_turn=True, has_winner=True)
        expected = False

        result = sut()

        assert result == expected

    def test_when_has_no_turn__no_winner__is_false(self, sut, state, local_store) -> None:
        local_store.state = state(has_turn=False, has_winner=False)
        expected = False

        result = sut()

        assert result == expected

    def test_when_has_no_turn__has_winner__is_false(
        self, sut, state, local_store
    ) -> None:
        local_store.state = state(has_turn=False, has_winner=True)
        expected = False

        result = sut()

        assert result == expected


class TestHasTurnNoWinnerTilesSelectionMode:
    @pytest.fixture()
    def sut(self, store, user_1, local_store) -> HasTurnNoWinnerTilesSelectionMode:
        store.state = State(current_user=user_1)
        return HasTurnNoWinnerTilesSelectionMode(store=store, local_store=local_store)

    def test_when_has_turn__no_winner__tiles_selection__is_true(
        self, sut, state, local_store
    ) -> None:
        local_store.state = state(
            has_turn=True, has_winner=False, selection_mode=SelectionMode.TILES
        )
        expected = True

        result = sut()

        assert result == expected

    def test_when_has_turn__no_winner__tilesets_selection__is_false(
        self, sut, state, local_store
    ) -> None:
        local_store.state = state(
            has_turn=True, has_winner=True, selection_mode=SelectionMode.TILESETS
        )
        expected = False

        result = sut()

        assert result == expected


class TestHasTurnNoWinnerTilesetsSelectionMode:
    @pytest.fixture()
    def sut(self, store, user_1, local_store) -> HasTurnNoWinnerTilesetsSelectionMode:
        store.state = State(current_user=user_1)
        return HasTurnNoWinnerTilesetsSelectionMode(store=store, local_store=local_store)

    def test_when_has_turn__no_winner__tiles_selection__is_true(
        self, sut, state, local_store
    ) -> None:
        local_store.state = state(
            has_turn=True, has_winner=False, selection_mode=SelectionMode.TILESETS
        )
        expected = True

        result = sut()

        assert result == expected

    def test_when_has_turn__no_winner__tilesets_selection__is_false(
        self, sut, state, local_store
    ) -> None:
        local_store.state = state(
            has_turn=True, has_winner=True, selection_mode=SelectionMode.TILES
        )
        expected = False

        result = sut()

        assert result == expected


class TestHasWinner:
    @pytest.fixture()
    def sut(self, store, user_1, local_store) -> HasWinner:
        store.state = State(current_user=user_1)
        return HasWinner(store=store, local_store=local_store)

    def test_when_has_winner__is_true(self, sut, state, local_store) -> None:
        local_store.state = state(has_winner=True)
        expected = True

        result = sut()

        assert result == expected

    def test_when_has_no_winner__is_false(self, sut, state, local_store) -> None:
        local_store.state = state(has_winner=False)
        expected = False

        result = sut()

        assert result == expected
