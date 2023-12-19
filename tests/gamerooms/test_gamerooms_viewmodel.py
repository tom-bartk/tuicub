from unittest.mock import Mock, patch

import pytest

from src.tuicub.common.state import State
from src.tuicub.gamerooms.state import GameroomsState, SetGameroomsRowsAction
from src.tuicub.gamerooms.view import GameroomRowViewModel
from src.tuicub.gamerooms.viewmodel import GameroomsViewModel


@pytest.fixture()
def sut(store, local_store) -> GameroomsViewModel:
    return GameroomsViewModel(store=store, local_store=local_store)


class TestIsListEmpty:
    def test_when_no_global_state_changes__returns_false(self, sut) -> None:
        expected = False

        result = sut.is_list_empty()

        assert result == expected

    def test_when_global_state_changed_w_none_gamerooms__returns_false(self, sut) -> None:
        expected = False

        sut.on_state(State(gamerooms=None))
        result = sut.is_list_empty()

        assert result == expected

    def test_when_global_state_changed_w_nonempty_gamerooms__returns_false(
        self, sut
    ) -> None:
        expected = False

        sut.on_state(State(gamerooms=(Mock(), Mock())))
        result = sut.is_list_empty()

        assert result == expected

    def test_when_global_state_changed_w_empty_gamerooms__returns_true(self, sut) -> None:
        expected = True

        sut.on_state(State(gamerooms=()))
        result = sut.is_list_empty()

        assert result == expected


class TestRows:
    def test_returns_rows_from_local_state(
        self, sut, local_store, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        rows = (
            GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=False),
            GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=True),
            GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=False),
        )
        local_store.state = GameroomsState(rows=rows)

        result = sut.rows()

        assert result == rows


class TestOnGlobalState:
    def test_dispatches_set_gamerooms_rows_action_to_local_store(
        self, sut, local_store, gameroom_1, gameroom_2
    ) -> None:
        expected = SetGameroomsRowsAction(gamerooms=(gameroom_1, gameroom_2))

        sut.on_state(State(gamerooms=(gameroom_1, gameroom_2)))

        local_store.dispatch.assert_called_once_with(expected)

    def test_invalidates_app(self, sut, get_app, app) -> None:
        with patch("prompt_toolkit.application.get_app", new=get_app):
            sut.on_state(State())

            app.invalidate.assert_called_once()


class TestOnLocalState:
    def test_invalidates_app(self, sut, get_app, app) -> None:
        with patch("prompt_toolkit.application.get_app", new=get_app):
            sut.on_state(GameroomsState())

            app.invalidate.assert_called_once()


class TestSubscribe:
    def test_subscribes_to_global_and_local_stores(self, sut, store, local_store) -> None:
        sut.subscribe()

        store.subscribe.assert_called_once_with(sut, include_current=True)
        local_store.subscribe.assert_called_once_with(sut, include_current=True)


class TestUnsubscribe:
    def test_unsubscribes_from_global_and_local_stores(
        self, sut, store, local_store
    ) -> None:
        sut.unsubscribe()

        store.unsubscribe.assert_called_once_with(sut)
        local_store.unsubscribe.assert_called_once_with(sut)
