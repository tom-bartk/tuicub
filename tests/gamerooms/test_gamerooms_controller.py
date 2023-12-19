from unittest.mock import Mock, patch

import pytest

from src.tuicub.common.state import State
from src.tuicub.common.views import ScrollDirection
from src.tuicub.gamerooms.controller import GameroomsController
from src.tuicub.gamerooms.requests import (
    CreateGameroomInteractor,
    GetGameroomsInteractor,
    JoinGameroomInteractor,
)
from src.tuicub.gamerooms.state import ScrollGameroomsAction


@pytest.fixture()
def create_gameroom_interactor() -> CreateGameroomInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def join_gameroom_interactor() -> JoinGameroomInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def get_gamerooms_interactor() -> GetGameroomsInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def sut(
    store,
    local_store,
    get_gamerooms_interactor,
    join_gameroom_interactor,
    create_gameroom_interactor,
) -> GameroomsController:
    return GameroomsController(
        store=store,
        local_store=local_store,
        get_gamerooms_interactor=get_gamerooms_interactor,
        join_gameroom_interactor=join_gameroom_interactor,
        create_gameroom_interactor=create_gameroom_interactor,
    )


class TestScreenDidPresent:
    def test_refreshes_gamerooms_list(self, sut, get_gamerooms_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.screen_did_present(screen=Mock())

            mock_async_run.assert_called_once()
            get_gamerooms_interactor.execute.assert_called_once()


class TestRefreshGamerooms:
    def test_refreshes_gamerooms_list(self, sut, event, get_gamerooms_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.refresh_gamerooms(event)

            mock_async_run.assert_called_once()
            get_gamerooms_interactor.execute.assert_called_once()


class TestScrollGameroomsDown:
    def test_dispatches_scroll_gamerooms_action_to_local_store_with_direction_down(
        self, sut, local_store, event
    ) -> None:
        expected = ScrollGameroomsAction(ScrollDirection.DOWN)

        sut.scroll_gamerooms_down(event)

        local_store.dispatch.assert_called_once_with(expected)


class TestScrollGameroomsUp:
    def test_dispatches_scroll_gamerooms_action_to_local_store_with_direction_up(
        self, sut, local_store, event
    ) -> None:
        expected = ScrollGameroomsAction(ScrollDirection.UP)

        sut.scroll_gamerooms_up(event)

        local_store.dispatch.assert_called_once_with(expected)


class TestJoinGameroom:
    def test_when_global_state_has_not_loaded_gamerooms__does_not_try_joining(
        self, sut, local_store, store, event, join_gameroom_interactor
    ) -> None:
        store.state = State(gamerooms=None)

        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.join_gameroom(event)

            mock_async_run.assert_not_called()
            join_gameroom_interactor.execute.assert_not_called()

    def test_when_global_state_has_empty_gamerooms__does_not_try_joining(
        self, sut, local_store, store, event, join_gameroom_interactor
    ) -> None:
        store.state = State(gamerooms=())

        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.join_gameroom(event)

            mock_async_run.assert_not_called()
            join_gameroom_interactor.execute.assert_not_called()

    def test_when_global_state_has_gamerooms__executes_join_gameroom_request(
        self, sut, local_store, store, event, join_gameroom_interactor
    ) -> None:
        store.state = State(gamerooms=(Mock(), Mock()))

        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.join_gameroom(event)

            mock_async_run.assert_called_once()
            join_gameroom_interactor.execute.assert_called_once()


class TestCreateGameroom:
    def test_executes_create_gameroom_request(
        self, sut, event, create_gameroom_interactor
    ) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.create_gameroom(event)

            mock_async_run.assert_called_once()
            create_gameroom_interactor.execute.assert_called_once()
