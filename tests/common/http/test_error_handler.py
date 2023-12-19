from unittest.mock import Mock, create_autospec

import httpx
import pytest
from marshmallow.exceptions import MarshmallowError

from src.tuicub.common.http import AlertErrorHandler
from src.tuicub.common.models import Alert, AlertType
from src.tuicub.common.strings import SERIALIZATION_ERROR_MESSAGE, UNKNOWN_ERROR_MESSAGE


@pytest.fixture()
def sut(alert_service) -> AlertErrorHandler:
    return AlertErrorHandler(alert_service=alert_service)


@pytest.mark.asyncio()
class TestHandle:
    async def test_when_http_status_error__json_has_message__queues_alert_with_message(
        self, sut, alert_service
    ) -> None:
        response = create_autospec(httpx.Response)
        response.text = '{"message": "foo"}'
        error = httpx.HTTPStatusError(message="bar", request=Mock(), response=response)

        await sut.handle(error)

        alert_service.queue_alert.assert_called_once_with(Alert("foo", AlertType.ERROR))

    async def test_when_http_status_error__json_has_no_message__queues_unkown_error_alert(
        self, sut, alert_service
    ) -> None:
        response = create_autospec(httpx.Response)
        response.text = '{"foo": "bar"}'
        error = httpx.HTTPStatusError(message="baz", request=Mock(), response=response)

        await sut.handle(error)

        alert_service.queue_alert.assert_called_once_with(
            Alert(UNKNOWN_ERROR_MESSAGE.format("baz"), AlertType.ERROR)
        )

    async def test_when_marshmallow_error__queues_serialization_error_alert(
        self, sut, alert_service
    ) -> None:
        await sut.handle(MarshmallowError())

        alert_service.queue_alert.assert_called_once_with(
            Alert(SERIALIZATION_ERROR_MESSAGE, AlertType.ERROR)
        )

    async def test_when_not_http_status_or_marshmallow_error__queues_error_string_alert(
        self, sut, alert_service
    ) -> None:
        await sut.handle(ValueError(42))

        alert_service.queue_alert.assert_called_once_with(
            Alert(str(ValueError(42)), AlertType.ERROR)
        )
