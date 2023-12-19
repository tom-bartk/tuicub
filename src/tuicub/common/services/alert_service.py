from typing import Protocol
from weakref import ReferenceType, ref

from ..models import Alert


class AlertServiceDelegate(Protocol):
    """Delegate that is notified whenever an alert is queued."""

    def did_queue_alert(self, alert: Alert) -> None:
        """Called whenever an alert is queued.

        Args:
            alert (Alert): The queued alert.
        """


class AlertService:
    """The service that handles queueing of alerts."""

    __slots__ = ("_delegate",)

    def __init__(self) -> None:
        self._delegate: ReferenceType[AlertServiceDelegate] | None = None

    def queue_alert(self, alert: Alert) -> None:
        """Queue an alert.

        The displaying of the alert is delegated to the `AlertServiceDelegate`.

        Args:
            alert (Alert): The alert to enqueue.
        """
        if self._delegate and (delegate := self._delegate()):
            delegate.did_queue_alert(alert=alert)

    def set_delegate(self, delegate: AlertServiceDelegate) -> None:
        self._delegate = ref(delegate)
