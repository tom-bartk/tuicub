from unittest.mock import Mock, patch

import pytest

from src.tuicub.gameroom.controller import GameroomController
from src.tuicub.gameroom.requests import (
    DeleteGameroomInteractor,
    LeaveGameroomInteractor,
    StartGameInteractor,
)


@pytest.fixture()
def delete_gameroom_interactor() -> DeleteGameroomInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def leave_gameroom_interactor() -> LeaveGameroomInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def start_game_interactor() -> StartGameInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def sut(
    store,
    leave_gameroom_interactor,
    delete_gameroom_interactor,
    start_game_interactor,
) -> GameroomController:
    return GameroomController(
        store=store,
        leave_gameroom_interactor=leave_gameroom_interactor,
        delete_gameroom_interactor=delete_gameroom_interactor,
        start_game_interactor=start_game_interactor,
    )


class TestLeaveGameroom:
    def test_executes_leave_gameroom_request(
        self, sut, event, leave_gameroom_interactor
    ) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.leave_gameroom(event)

            mock_async_run.assert_called_once()
            leave_gameroom_interactor.execute.assert_called_once()


class TestDeleteGameroom:
    def test_executes_delete_gameroom_request(
        self, sut, event, delete_gameroom_interactor
    ) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.delete_gameroom(event)

            mock_async_run.assert_called_once()
            delete_gameroom_interactor.execute.assert_called_once()


class TestStartGameroom:
    def test_executes_start_game_request(self, sut, event, start_game_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.start_game(event)

            mock_async_run.assert_called_once()
            start_game_interactor.execute.assert_called_once()
