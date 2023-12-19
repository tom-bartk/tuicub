import json

import httpx
from httperactor import ErrorHandler
from marshmallow.exceptions import MarshmallowError

from ..models import Alert, AlertType
from ..services.alert_service import AlertService
from ..strings import SERIALIZATION_ERROR_MESSAGE, UNKNOWN_ERROR_MESSAGE


class AlertErrorHandler(ErrorHandler):
    """An error handler that displays errors as alerts."""

    __slots__ = ("_alert_service",)

    def __init__(self, alert_service: AlertService):
        self._alert_service: AlertService = alert_service

    async def handle(self, error: Exception) -> None:
        """Handle error.

        Converts the error into an alert and queues it.

        Args:
            error (Exception): The error to handle.
        """
        if isinstance(error, httpx.HTTPStatusError):
            error_data = json.loads(error.response.text)
            message = error_data.get("message", None) or UNKNOWN_ERROR_MESSAGE.format(
                str(error)
            )
            self._alert_service.queue_alert(Alert(message, AlertType.ERROR))
        elif isinstance(error, MarshmallowError):
            self._alert_service.queue_alert(
                Alert(SERIALIZATION_ERROR_MESSAGE, AlertType.ERROR)
            )
        else:
            self._alert_service.queue_alert(Alert(str(error), AlertType.ERROR))
