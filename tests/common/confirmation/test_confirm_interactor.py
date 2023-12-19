from unittest.mock import create_autospec

import pytest

from src.tuicub.app.state import AppState
from src.tuicub.common.confirmation import Confirmation, ConfirmInteractor


@pytest.fixture()
def sut(app_store) -> ConfirmInteractor:
    return ConfirmInteractor(store=app_store)


class TestAnswerConfirmation:
    def test_when_app_state_has_confirmation__answers_it(self, sut, app_store) -> None:
        confirmation = create_autospec(Confirmation)
        app_store.state = AppState(confirmation=confirmation)
        exptected = True

        sut.answer_confirmation(answer=exptected)

        confirmation.answer.assert_called_once_with(exptected)
