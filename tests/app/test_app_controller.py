from unittest.mock import create_autospec

import pytest

from src.tuicub.app.controller import AppController
from src.tuicub.common.confirmation import ConfirmInteractor


@pytest.fixture()
def confirm_interactor() -> ConfirmInteractor:
    return create_autospec(ConfirmInteractor)


@pytest.fixture()
def sut(confirm_interactor) -> AppController:
    return AppController(confirm_interactor=confirm_interactor)


class TestAnswerConfirmationYes:
    def test_calls_confirm_interactor_with_true_answer(
        self, sut, confirm_interactor, event
    ) -> None:
        sut.answer_confirmation_yes(event)

        confirm_interactor.answer_confirmation.assert_called_once_with(answer=True)


class TestAnswerConfirmationNo:
    def test_calls_confirm_interactor_with_false_answer(
        self, sut, confirm_interactor, event
    ) -> None:
        sut.answer_confirmation_no(event)

        confirm_interactor.answer_confirmation.assert_called_once_with(answer=False)
