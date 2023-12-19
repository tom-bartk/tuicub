from unittest.mock import create_autospec

import pytest

from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.services.alert_service import AlertService, AlertServiceDelegate


@pytest.fixture()
def delegate() -> AlertServiceDelegate:
    return create_autospec(AlertServiceDelegate)


@pytest.fixture()
def sut() -> AlertService:
    return AlertService()


class TestQueueAlert:
    def test_when_delegate_set__calls_did_queue_alert_on_delegate(
        self, sut, delegate
    ) -> None:
        sut.set_delegate(delegate)
        sut.queue_alert(Alert("foo", AlertType.INFO))

        delegate.did_queue_alert.assert_called_once_with(Alert("foo", AlertType.INFO))
