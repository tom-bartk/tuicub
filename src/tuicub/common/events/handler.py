from typing import Generic, TypeVar

from eventoolkit import Event, StoreEventHandler
from pydepot import Store

from ..services.alert_service import AlertService
from ..state import State

TEvent = TypeVar("TEvent", bound=Event)


class AlertingStoreEventHandler(Generic[TEvent], StoreEventHandler[TEvent, State]):
    """Base event handler that uses the alert service."""

    __slots__ = ("_alert_service",)

    def __init__(self, alert_service: AlertService, store: Store[State]):
        self._alert_service: AlertService = alert_service
        super().__init__(store=store)
