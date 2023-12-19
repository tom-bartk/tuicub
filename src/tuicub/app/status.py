from __future__ import annotations

from weakref import WeakMethod

from attrs import evolve, frozen
from prompt_toolkit import application

from ..common.confirmation.confirmation import Confirmation
from ..common.models import Alert
from ..common.views import Color, Text, TextView, Theme
from ..common.views.animation import TextAnimator
from ..common.views.text import EMPTY_TEXT


class StatusViewModel:
    """A viewmodel for the status view."""

    __slots__ = ("_animator", "_status_content", "__weakref__")

    def __init__(self, animator: TextAnimator) -> None:
        self._animator: TextAnimator = animator
        self._status_content: StatusContent = StatusContent(
            alert_animation_frame=None, confirmation=None
        )

    def status_content(self) -> Text:
        """Returns the text content of the status view."""
        return self._status_content.text()

    def status_background(self) -> Color | None:
        """Returns the optional background color of the status view."""
        return self._status_content.background_color()

    def set_confirmation(self, confirmation: Confirmation | None) -> None:
        """Sets the confirmation to display on the status view."""
        self._status_content = evolve(self._status_content, confirmation=confirmation)
        application.get_app().invalidate()

    def did_queue_alert(self, alert: Alert) -> None:
        """Callback of the `AlertServiceDelegate` called whenever an alert is queued.

        Performs an animation returned by the alert.

        Args:
            alert (Alert): The queued alert.
        """
        self._animator.animate(
            animation=alert.animation, side_effect=WeakMethod(self.on_alert_text)
        )

    def on_alert_text(self, text: Text) -> None:
        """The side effect for the alert animation."""
        self._status_content = evolve(self._status_content, alert_animation_frame=text)


class StatusView(TextView):
    """The status view displaying alerts and confirmations."""

    def __init__(self, viewmodel: StatusViewModel, theme: Theme | None = None):
        super().__init__(
            text=viewmodel.status_content,
            background_color=viewmodel.status_background,
            theme=theme,
        )


@frozen
class StatusContent:
    """A wrapper for the status text content."""

    alert_animation_frame: Text | None
    confirmation: Confirmation | None

    def text(self) -> Text:
        if self.confirmation:
            return self.confirmation.ui_text
        elif self.alert_animation_frame:
            return self.alert_animation_frame
        return EMPTY_TEXT

    def background_color(self) -> Color | None:
        if self.confirmation:
            return Color.RED_DIM
        return Color.BG0
