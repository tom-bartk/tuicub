from unittest.mock import Mock, patch

import pytest

from src.tuicub.game.interactors.actions import ActionsInteractor
from src.tuicub.game.requests.draw import DrawRequestInteractor
from src.tuicub.game.requests.end_turn import EndTurnRequestInteractor
from src.tuicub.game.requests.move import MoveRequestInteractor
from src.tuicub.game.requests.redo import RedoRequestInteractor
from src.tuicub.game.requests.undo import UndoRequestInteractor


@pytest.fixture()
def move_interactor() -> MoveRequestInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def end_turn_interactor() -> EndTurnRequestInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def draw_interactor() -> DrawRequestInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def undo_interactor() -> UndoRequestInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def redo_interactor() -> RedoRequestInteractor:
    interactor = Mock()
    interactor.execute = Mock()
    return interactor


@pytest.fixture()
def sut(
    draw_interactor,
    end_turn_interactor,
    move_interactor,
    redo_interactor,
    undo_interactor,
) -> ActionsInteractor:
    return ActionsInteractor(
        draw_interactor=draw_interactor,
        end_turn_interactor=end_turn_interactor,
        move_interactor=move_interactor,
        redo_interactor=redo_interactor,
        undo_interactor=undo_interactor,
    )


class TestDraw:
    def test_executes_draw_request(self, sut, draw_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.draw()

            mock_async_run.assert_called_once()
            draw_interactor.execute.assert_called_once()


class TestEndTurn:
    def test_executes_end_turn_request(self, sut, end_turn_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.end_turn()

            mock_async_run.assert_called_once()
            end_turn_interactor.execute.assert_called_once()


class TestMoveTiles:
    def test_executes_move_request(self, sut, move_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.move_tiles()

            mock_async_run.assert_called_once()
            move_interactor.execute.assert_called_once()


class TestRedo:
    def test_executes_redo_request(self, sut, redo_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.redo()

            mock_async_run.assert_called_once()
            redo_interactor.execute.assert_called_once()


class TestUndo:
    def test_executes_undo_request(self, sut, undo_interactor) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.undo()

            mock_async_run.assert_called_once()
            undo_interactor.execute.assert_called_once()
